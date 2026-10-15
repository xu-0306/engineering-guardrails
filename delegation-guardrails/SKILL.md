---
name: delegation-guardrails
description: "Hand work to another coding agent and accept it back without plan drift or masked failures. Use when writing a brief for an implementer (Codex, a subagent, another session), monitoring its run, or reviewing what it returns: briefs that leave the environment, reference model, or affected callers for the implementer to invent; implementers that get green by weakening assertions, adding !important or inline styles, swallowing errors, or string-matching their own messages; reviewers that trust the report or silently take over. Not for doing the implementation yourself."
---

# Delegation Guardrails

An implementer optimizes for what the brief and the checks reward. Written rules are weakest exactly when it is under pressure to get green, so put the expectations that matter into commands it must run and checks it cannot edit, and review the diff rather than the report. This skill applies once delegation was chosen; it does not require or authorize delegating.

## Before Handing Off: Leave Nothing to Invent

- Take the outcome and acceptance criteria from what the user agreed. Name what is out of scope. Size each brief to one usable, separately verifiable result (roughly 30–45 minutes of work); split larger work into stages.
- Read the reference model first. When a mature reference or an existing module already solves the concern, read how it defines and routes the thing as a whole (types, flow, ownership), not only its edge rules. Name the exact file paths in the brief and ask for a short note on deviations. Do not write a rule the reference does without unless a stated requirement needs it.
- Define cross-cutting shapes once (error envelope, status names, shared components) in the first stage that touches them; later briefs reference that definition.
- Before a brief removes, replaces, unifies, or narrows X (a whitelist, a stricter validator, a changed default at a shared boundary), list what depends on X: callers, registrations, messages that only exist because of X, and tests. For a shared boundary, list both sides: everything that feeds it and everything that reads its output. Build the list with a search, not from memory, and put the command and its hit count in the brief so the reviewer can rerun it. An unlisted dependent is where the next regression comes from.
- Give runnable commands with the full environment block (variables, interpreter, paths). A check that cannot start silently turns verification off. Say which checks run during work, which run at hand-off, and which are left for integration. When the change touches a shared surface (a display format, an error shape, a component), the related checks are the ones that assert on that surface's output, found by searching for its selectors, fields, or messages, not the tests next to the edited files.
- State the stop rule and the assertion rule: the same assertion failing twice means stop and write the root cause; assertions may only be replaced equivalently or tightened, each listed old → new. Name the masking patterns that are not acceptable fixes for this stack.
- Check the implementer's own loaded instructions for conflicts, such as stale copies of these guardrails or skills that push "never give up" against the stop rule.

[references/brief-template.md](references/brief-template.md) is a starting point; keep only the parts this task needs.

## While It Runs

- Detect completion from a structural signal: process exit, an exact marker on the last log line, or the result file. Never infer it from text the output may quote.
- Report progress at the agreed interval. If the run stops or fails, bring the root cause and options to the user before fixing it yourself, unless the user said otherwise. Taking over silently hides whether the brief or the plan was wrong.
- Work by others in a shared checkout is not yours to edit or revert.

## When It Comes Back: Diff First, Report Second

1. Run `scripts/scan_masking.py --repo <checkout> --base <restore point>` (or pipe any diff with `-`). Each finding needs a reason or a change; findings are prompts, not verdicts. The assertion check counts lines, so it cannot see a condition loosened in place (`==` → `>=`): read every assertion change.
2. Compare the diff with the brief item by item: requested behavior present, nothing added outside scope, replacements finished (old path and its references gone, no parallel version). Rerun the brief's dependent search on the result; every remaining hit is handled, or the brief said why it stays.
3. Where a fix guesses, wraps, or matches text, ask what typed or structural signal already exists. Apply anti-hardcode-engineering and anti-complexity-engineering at that boundary.
4. Re-run the checks whose numbers matter. A check that never started (missing module, missing variable) is unverified, not failed and not passed.
5. Commit a restore point before the next dispatch. Run the expensive full verification once at integration.

## Limits

This guidance is advisory and can be skipped under pressure. Put the few rules that must hold into places that are enforced or always loaded: the scan as an acceptance gate, lint rules (for example stylelint `declaration-no-important`, ruff `BLE001`/`S110`), protected test paths, CI, and a short repository `AGENTS.md`/`CLAUDE.md`. Add a check only for a failure that has actually occurred.
