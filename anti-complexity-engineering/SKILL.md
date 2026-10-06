---
name: anti-complexity-engineering
description: Keep architecture and plans proportional when designing or reviewing changes that add entities, states, layers, or parallel lifecycles, or when a bug fix adds another wrapper. Detect scope drift and unnecessary completion gates in that work. Skip mechanical edits.
---

# Anti-Complexity Engineering

Deliver the user's requested outcome with the fewest concepts and steps that actually serve it. Apply this guidance within the task; it does not require a separate audit, specification, or approval phase.

## Keep the Outcome Fixed

- Use the user's requested behavior and agreed acceptance criteria as the definition of done. If they are clear, proceed; do not require another specification or confirmation.
- Add work only when it serves that outcome or is a necessary dependency. Explain a newly discovered dependency in terms of what it blocks. Optional improvements must not block delivery.
- Do not silently raise the acceptance bar or turn an implementation preference into a product requirement. Incorporate user-approved scope changes; ask only when a material ambiguity cannot be resolved from context.
- Reassess inherited plans, agent suggestions, and old TODOs against the current goal. They are not automatically requirements.
- Once the requested outcome works and necessary verification passes, deliver it. Do not extend the task with speculative hardening or cleanup.

## Reuse Before Adding Concepts

A concept is something a maintainer must learn: an entity, state, table, configuration field, protocol, layer, or pass on every request.

- Understand the affected flow and callers, then express the change using existing primitives. Prefer existing code, standard libraries, native platform features, and installed dependencies before adding machinery.
- Give each new concept a concrete requirement. A second lifecycle for the same idea, duplicated derived state, or a prediction enforced by another gate needs particular scrutiny.
- Use a mature reference when an unfamiliar architectural choice would benefit from comparison. Existing code or a dependency may suffice; routine fixes do not require external research. Compare requirements as well as size.
- Treat unused configuration, single-implementation abstractions, and statuses with no behavioral effect as simplification candidates. Check their purpose before removing them.
- A short explanation usually suffices. Use a concept table only when several additions or tradeoffs make it useful, not as a condition of approval.

## Fix the Cause and Remove Redundancy

- Trace the failure to its cause and repair it where affected callers share the behavior. Avoid another verifier, fallback, or wrapper that only hides the defect.
- Inspect a layer's callers, tests, and purpose before removing it. The fact that a bug disappears when a layer is removed does not prove the layer is unnecessary.
- Keep boundaries that constrain permissions or validate untrusted input. For layers that duplicate decisions or derived state, consider merging or deleting them when their purpose is already served elsewhere.
- Remove paths made obsolete by this change when safe. Do not force unrelated deletions to make a fix look simpler, or start a broader rewrite to avoid a justified local repair.
- Record a deferred removal only when a concrete unresolved risk or migration dependency needs follow-up. No mandatory deletion ledger or removal commitment for every bug fix.

## Keep Planning and Verification Proportional

- Small changes need direct execution and an appropriate check, not staged specifications, inventories, or readiness gates. Larger plans should lead to usable outcomes and include necessary investigation without turning each finding into a new phase.
- Deliver the complete requested flow. A thin implementation may reduce machinery, but must not omit explicitly requested behavior or necessary dependencies.
- Use delegation, extra review, or a migration plan only when the task benefits. Keep migration coexistence bounded by an actual dependency; remove the replaced path when safe.
- Tests verify requirements; they do not create them. On failure, distinguish an implementation defect, an obsolete test, and a test asserting behavior outside the agreed scope. Preserve valid regression coverage; do not weaken checks merely to get a pass.
- Run checks appropriate to the affected behavior and risk. Broaden or repeat them when changes, failures, or unresolved concerns justify it, not to keep a completed task active.
- For a handoff, briefly state the goal, what works, the remaining required gap, and the next useful outcome. Reuse existing notes rather than adding parallel progress documents.

## Preserve Necessary Complexity

Keep explicitly requested behavior, accessibility, trust-boundary validation, authorization, required approvals, sandboxing, secret handling, and error handling that prevents data loss. Preserve necessary transactions, undo, backups, migrations, inherent concurrency controls, required audit obligations, and performance work supported by measurements. Keep each responsibility in one place where practical.

Other skills may help with a specific problem, but their templates and recommended workflows must not expand the user's task. Apply only the guidance relevant to the actual change; do not stack every available planning, review, and verification workflow.

## When Asked to Audit

Investigate the requested scope and affected flows. Look for duplicate lifecycles, redundant derived state, repeated platform functionality, unused paths, and process work that blocks usable results. File size and architectural vocabulary are clues, not proof. Tests and evaluation tooling can have legitimate consumers outside production.

Report the strongest supported simplification candidates, the behavior they must preserve, and relevant uncertainty. Do not turn an audit into an unrequested rewrite or mandatory freeze.

## Reporting

Explain the outcome, any material design tradeoff, the verification performed, and remaining limitations. Mention additions, deletions, references, or deferred work only when they help assess the change. No fixed report fields, concept counts, or bookkeeping artifacts are required.
