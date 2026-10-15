#!/usr/bin/env python3
"""List diff lines that commonly hide a problem instead of fixing it.

Findings are review prompts, not verdicts: each one needs a reason in the
hand-off report or a change. Reads a unified diff from a file or stdin, or runs
`git diff <base>` (plus untracked files) in a repository.

Usage:
  python scan_masking.py                      # working tree vs HEAD, incl. untracked
  python scan_masking.py --base main          # working tree vs main
  python scan_masking.py --repo PATH --base REF
  git diff A B | python scan_masking.py -     # any diff on stdin
  python scan_masking.py changes.diff --report-only

Exit code: 1 when findings exist (use as a gate), 0 otherwise or with --report-only.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

STYLE_FILES = re.compile(r"\.(css|scss|sass|less|html|vue|svelte|[jt]sx?)$", re.I)
MARKUP_FILES = re.compile(r"\.(html|vue|svelte|[jt]sx)$", re.I)
TEST_PATH = re.compile(r"(^|/)(tests?|e2e|__tests__|spec)(/|$)|(^|/)test_[^/]+\.py$|_test\.(py|go)$|\.(test|spec)\.[cm]?[jt]sx?$", re.I)
ASSERTION = re.compile(r"\bassert\w*\b|\bexpect\s*\(|self\.assert\w+\s*\(|\.to(Be|Equal|Match|Contain|Throw|Have)\w*\s*\(|\bwaitFor\s*\(")
ERROR_NAME = r"\b(?:err(?:or)?|exc(?:eption)?|cause|e)\b"

RULES = [
    ("important", "CSS !important added", STYLE_FILES, re.compile(r"!important")),
    ("inline-style", "inline style added", MARKUP_FILES, re.compile(r"\bstyle\s*=\s*(\{\{|\"|')")),
    ("broad-except", "broad or bare except added", re.compile(r"\.py$"), re.compile(r"^\s*except\s*(:|\(?\s*(Base)?Exception\b)")),
    ("swallow", "error swallowed (pass / empty catch)", None,
     re.compile(r"^\s*except\b.*:\s*(pass|\.\.\.)\s*$|catch\s*(\([^)]*\))?\s*\{\s*\}|\.catch\s*\(\s*\(\s*\w*\s*\)\s*=>\s*(\{\s*\}|undefined|null)\s*\)")),
    ("skip-test", "test skipped or focused", None,
     re.compile(r"@(unittest\.)?skip|pytest\.mark\.(skip|xfail)|\b(it|test|describe)\.(skip|only)\s*\(|\bx(it|describe|test)\s*\(")),
    ("suppression", "checker suppressed", None,
     re.compile(r"#\s*(type:\s*ignore|noqa|pragma:\s*no cover)|@ts-(ignore|expect-error|nocheck)|eslint-disable|biome-ignore|stylelint-disable")),
    ("message-match", "decision made by matching error text", None,
     re.compile(r"(['\"][^'\"]{3,}['\"]\s+in\s+(str\(\s*" + ERROR_NAME + r"\s*\)|" + ERROR_NAME + r"\.(message|args)|\w*(message|detail|text|lower)\w*(\(\))?\b)"
                r"|(" + ERROR_NAME + r"|message|detail)\w*\s*\.\s*(includes|startsWith|endsWith|startswith|endswith)\s*\(\s*['\"]"
                r"|String\(\s*" + ERROR_NAME + r"\s*\)\s*\.\s*(includes|match)\s*\()", re.I)),
    ("script-detect", "behaviour chosen by detecting a writing system", None,
     re.compile(r"\\u4e00|\u4e00-|\\u0400|\u0400-|\\p\{(Han|Script=)|\\u3040|\\uac00")),
]


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True).stdout.decode("utf-8", "replace")


def collect_diff(args) -> str:
    if args.diff:
        data = sys.stdin.buffer.read() if args.diff == "-" else Path(args.diff).read_bytes()
        return data.decode("utf-8", "replace")
    repo = Path(args.repo)
    text = git(repo, "diff", "--no-color", "--no-ext-diff", args.base)
    for name in git(repo, "ls-files", "--others", "--exclude-standard").splitlines():
        path = repo / name
        try:
            body = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        lines = body.splitlines()
        text += f"\ndiff --git a/{name} b/{name}\n--- /dev/null\n+++ b/{name}\n@@ -0,0 +1,{len(lines)} @@\n"
        text += "".join(f"+{line}\n" for line in lines)
    return text


def scan(diff: str):
    findings = []
    asserts = defaultdict(lambda: [0, 0])  # path -> [removed, added]
    deleted_tests = []
    path, old_path, old_no, new_no = None, "", 0, 0
    for raw in diff.splitlines():
        if raw.startswith("diff --git"):
            path = None
            continue
        if raw.startswith("--- "):
            old_path = raw[4:].strip()
            continue
        if raw.startswith("+++ "):
            target = raw[4:].strip()
            if target == "/dev/null":
                path = old_path[2:] if old_path.startswith("a/") else old_path
                if TEST_PATH.search(path):
                    deleted_tests.append(path)
            else:
                path = target[2:] if target.startswith("b/") else target
            continue
        hunk = re.match(r"@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", raw)
        if hunk:
            old_no, new_no = int(hunk.group(1)), int(hunk.group(2))
            continue
        if path is None or not raw or raw[0] not in "+- ":
            continue
        line, sign = raw[1:], raw[0]
        if sign == " ":
            old_no += 1
            new_no += 1
            continue
        if TEST_PATH.search(path) and ASSERTION.search(line):
            asserts[path][0 if sign == "-" else 1] += 1
        if sign == "-":
            old_no += 1
            continue
        for rule_id, label, files, pattern in RULES:
            if files is not None and not files.search(path):
                continue
            if rule_id == "message-match" and TEST_PATH.search(path):
                continue  # tests assert on visible text by design
            if pattern.search(line):
                findings.append((path, new_no, rule_id, label, line.strip()[:160]))
        new_no += 1
    for path, (removed, added) in sorted(asserts.items()):
        if removed > added:
            findings.append((path, 0, "assertions-down", f"assertion lines {removed} removed / {added} added", "list each change as old -> new"))
    for path in deleted_tests:
        findings.append((path, 0, "test-deleted", "test file deleted", ""))
    return findings


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("diff", nargs="?", help="diff file, or - for stdin; omit to run git diff")
    parser.add_argument("--repo", default=".", help="repository for git mode (default: .)")
    parser.add_argument("--base", default="HEAD", help="git diff base in git mode (default: HEAD)")
    parser.add_argument("--report-only", action="store_true", help="always exit 0")
    args = parser.parse_args()
    findings = scan(collect_diff(args))
    for path, line, rule_id, label, snippet in findings:
        location = f"{path}:{line}" if line else path
        print(f"{location}  [{rule_id}] {label}" + (f"\n    {snippet}" if snippet else ""))
    counts = defaultdict(int)
    for item in findings:
        counts[item[2]] += 1
    summary = ", ".join(f"{key} {value}" for key, value in sorted(counts.items())) or "none"
    print(f"\n{len(findings)} finding(s): {summary}")
    return 1 if findings and not args.report_only else 0


if __name__ == "__main__":
    sys.exit(main())
