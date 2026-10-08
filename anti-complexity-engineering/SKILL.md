---
name: anti-complexity-engineering
description: Keep implementation, defensive logic, and verification proportional when designing, fixing, replacing, or reviewing code. Use for unnecessary layers or fallbacks, expanding test scope, incomplete replacement of old paths, and dead code left by a change. Complete affected callers and cleanup without turning a local fix into a whole-repository audit. Scale down for mechanical edits.
---

# Anti-Complexity Engineering

Deliver the user's requested outcome with the fewest concepts and steps that actually serve it. Apply this guidance within the task; it does not require a separate audit, specification, or approval phase.

**For replacement work, a working new path is not the finish line.** Before delivering, inspect the old path's remaining references. For each, either identify the supported behavior that still requires it, or update/remove that reference and the now-unused implementation. A leftover registration or test is not its own justification for retention. Do this within the affected flow, not as a whole-repository sweep.

## Keep the Outcome Fixed

- Use the user's requested behavior and agreed acceptance criteria as the definition of done. If they are clear, proceed; do not require another specification or confirmation.
- Add work only when it serves that outcome or is a necessary dependency. Explain a newly discovered dependency in terms of what it blocks. Optional improvements must not block delivery.
- Do not silently raise the acceptance bar or turn an implementation preference into a product requirement. Incorporate user-approved scope changes; ask only when a material ambiguity cannot be resolved from context.
- Reassess inherited plans, agent suggestions, and old TODOs against the current goal. They are not automatically requirements.
- Complete the requested behavior and the cleanup made necessary by this change, then deliver after the relevant checks pass. Removing what the change made obsolete is part of completion; speculative hardening and unrelated cleanup are not.

## Reuse Before Adding Concepts

A concept is something a maintainer must learn: an entity, state, table, configuration field, protocol, layer, or pass on every request.

- Understand the affected flow and callers, then express the change using existing primitives. Prefer existing code, standard libraries, native platform features, and installed dependencies before adding machinery.
- Give each new concept a concrete requirement. A second lifecycle for the same idea, duplicated derived state, or a prediction enforced by another gate needs particular scrutiny.
- Justify defensive checks, retries, fallbacks, and compatibility branches with a supported contract, known failure mode, reproducible fault, or concrete risk. An incident need not happen first, but "just in case" is not enough. Prefer repairing the cause over adding a fallback that silently continues through an obsolete path or masks failure as success.
- Use a mature reference when an unfamiliar architectural choice would benefit from comparison. Existing code or a dependency may suffice; routine fixes do not require external research. Compare requirements as well as size.
- Treat unused configuration, single-implementation abstractions, and statuses with no behavioral effect as simplification candidates. Check their purpose before removing them.
- A short explanation usually suffices. Use a concept table only when several additions or tradeoffs make it useful, not as a condition of approval.

## Fix the Cause and Remove Redundancy

- Trace the failure to its cause and repair it where affected callers share the behavior. Avoid another verifier, fallback, or wrapper that only hides the defect.
- Inspect a layer's callers, tests, and purpose before removing it. The fact that a bug disappears when a layer is removed does not prove the layer is unnecessary.
- Distinguish supported legacy behavior, incomplete replacement, and dead code. Preserve an old path for a concrete supported consumer, contract, or necessary side effect. Otherwise migrate remaining callers and remove the obsolete path; do not treat an optional configuration value or a test of retired internals as a compatibility requirement by itself.
- Finish the replacement through affected callers and entry points, including relevant routes, registries, configuration, exports, and build inputs. Remove the implementation and associated imports, styles, dependencies, fixtures, or current documentation made obsolete by this change. Moving code to a legacy directory while leaving active references does not finish the replacement. Do not delete user data, required migrations, or unrelated historical artifacts as code cleanup.
- Use existing compiler, lint, reference search, or dependency tools as evidence, not automatic deletion authority. Check relevant dynamic loading, registration, initialization side effects, public consumers, and test/build entry points. Zero text matches do not prove dead code; a group of mutually referencing files may still be unreachable from any effective entry point. Bound this investigation to the affected flow unless a broader audit was requested.
- Remove confirmed redundant paths without forcing unrelated deletions or a broader rewrite. If removal must wait, identify the concrete consumer or unresolved dependency and the condition that would permit removal in existing notes or a short comment. No mandatory deletion ledger, arbitrary deadline, or speculative compatibility layer.

## Keep Planning and Verification Proportional

- Small changes need direct execution and an appropriate check, not staged specifications, inventories, or readiness gates. Larger plans should lead to usable outcomes and include necessary investigation without turning each finding into a new phase.
- Deliver the complete requested flow. A thin implementation may reduce machinery, but must not omit explicitly requested behavior or necessary dependencies.
- Use delegation, extra review, or a migration plan only when the task benefits. Keep migration coexistence bounded by an actual dependency; remove the replaced path when safe.
- Tests verify requirements; they do not create them. On failure, distinguish an implementation defect, an obsolete test, and a test asserting behavior outside the agreed scope. Preserve valid regression coverage; do not weaken checks merely to get a pass.
- Preserve tests for supported behavior and compatibility. Adapt or remove assertions coupled only to retired internals, and remove fixtures with no remaining test consumer; do not keep obsolete production code solely to satisfy those assertions. Prefer observable results, while testing implementation details when they are themselves requirements, such as resource limits or caching.
- Reuse checks that already cover the change and add only missing evidence for affected behavior or concrete risk. Do not duplicate tests to increase counts, impose arbitrary coverage targets, or add a new test/scanning framework for routine cleanup. Check removals through relevant callers and behavior rather than adding tests that merely assert a file or symbol is absent, unless absence is itself a requirement.
- Run the applicable project-required checks and checks justified by the change. Once they pass, stop unless further edits, failures, or unresolved concerns justify another run or broader coverage. Keep required slow or full-suite checks; do not invent them for every small fix or rerun unchanged checks merely to strengthen a completion claim.
- For a handoff, briefly state the goal, what works, the remaining required gap, and the next useful outcome. Reuse existing notes rather than adding parallel progress documents.

## Preserve Necessary Complexity

Keep explicitly requested behavior, accessibility, trust-boundary validation, authorization, required approvals, sandboxing, secret handling, and error handling that prevents data loss. Preserve necessary transactions, undo, backups, migrations, inherent concurrency controls, required audit obligations, and performance work supported by measurements. Keep each responsibility in one place where practical.

Repeated validation is a redundancy candidate only when it protects the same invariant over the same representation within the same trust boundary, and callers cannot bypass the earlier guarantee. Separate boundaries or transformations may need separate checks: client validation does not replace server validation. Sharing validation logic must not remove enforcement at a required boundary.

Other skills may help with a specific problem, but their templates and recommended workflows must not expand the user's task. Apply only relevant guidance and let the same valid evidence satisfy overlapping requirements instead of duplicating suites or reviews. This does not waive explicit user or project requirements. Do not stack every available planning, review, and verification workflow.

## When Asked to Audit

Investigate the requested scope and affected flows. Look for duplicate lifecycles, redundant derived state, repeated platform functionality, unused paths, and process work that blocks usable results. File size and architectural vocabulary are clues, not proof. Tests and evaluation tooling can have legitimate consumers outside production.

Report the strongest supported simplification candidates, the behavior they must preserve, and relevant uncertainty. Do not turn an audit into an unrequested rewrite or mandatory freeze.

## Reporting

Explain the outcome, any material design tradeoff, the verification performed, and remaining limitations. Mention additions, deletions, references, or deferred work only when they help assess the change. No fixed report fields, concept counts, or bookkeeping artifacts are required.
