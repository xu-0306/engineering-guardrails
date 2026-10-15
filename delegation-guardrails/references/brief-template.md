# Brief Template

A starting point for an implementer brief. Delete sections the task does not need; a short brief that names the real constraints beats a long one.

## Goal

- Outcome: <what the user will be able to do, in their words>
- Acceptance: <the agreed criteria; nothing stricter>
- Out of scope: <related work that must not be touched or started>
- Time cap: <minutes>. If the cap is reached, stop and report what is done and what remains.

## Workspace and Rules

- Write only in <checkout/worktree>; reading elsewhere is fine. Do not commit, push, stash, reset, or install dependencies unless stated.
- Editable paths: <paths>. Keep each file's existing line endings and encoding.
- Same assertion fails twice: stop and write the root cause. Never delete or loosen an assertion; replace equivalently or tighten, and list each change as old → new.
- Not acceptable as fixes here: <e.g. !important or inline styles, broad except / empty catch, matching error message text, detecting a language or script to choose behavior, skipping tests, checker suppressions>.

## Reference

- Read first: <exact reference file paths> — follow its overall model for <concern>.
- Report deviations briefly: item / reference / ours / reason.

## Affected Dependents

<Only when removing, replacing, or unifying something.> Everything that depends on <X>, which must keep working or be migrated:

- <caller / registration / message / test>

## Tasks

1. <ordered; a later part starts only after the earlier part's checks pass>

## Environment

```text
<exact variables, interpreter, working directory; copy from a command that has run successfully>
```

## Verification

- During work: <type check + tests for the touched area>
- At hand-off: <full suite of each layer changed>
- Left for integration (do not run): <packaging, full end-to-end sweep>
- Pass means: <exit code 0 and the stated marker>; do not treat a wrapper's exit 0 as a pass.

## Report

Ask only for what the reviewer will check:

- What changed and what was deleted
- Assertion changes as old → new
- Commands run with exit codes and log paths; anything not run, marked as not verified
- Screenshots or outputs the implementer actually inspected
- If stopped: where, root cause, and two or three options
- Problems noticed outside the scope (UI, copy, design), as suggestions
