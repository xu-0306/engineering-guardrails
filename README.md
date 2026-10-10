# Engineering Guardrails

Skills for coding agents (Codex, Claude Code, and other agents that load `SKILL.md` folders) that keep implementations aligned with the user's requested outcome.

| Skill | Prevents | Use when |
|---|---|---|
| [anti-hardcode-engineering](anti-hardcode-engineering/) | fixes that are too narrow: keyword lists, copied examples, brittle selectors, provider strings | fixing a specific open-world bug at one boundary |
| [anti-complexity-engineering](anti-complexity-engineering/) | unnecessary layers or defenses, expanding test scope, incomplete replacements, and dead code left by a change | designing, fixing, replacing, or reviewing code with these risks |
| [ui-reference-fidelity](ui-reference-fidelity/) | drift from a chosen UI reference, incomplete interactions, and functional checks mistaken for UX acceptance | implementing a reference design or fixing a working-but-wrong interface |
| [memory-sanity-check](memory-sanity-check/) | stale assumptions steering decisions, old proposals becoming requirements, and repeated replanning | a consequential direction depends on prior context or conflicts with current evidence |

Use the skills relevant to the task. anti-hardcode-engineering chooses the right abstraction for one bug; anti-complexity-engineering keeps that abstraction and the surrounding workflow proportional to the requested outcome. ui-reference-fidelity preserves the chosen design and verifies visible interaction results without requiring a framework change or a full-product audit.

memory-sanity-check checks whether prior assumptions still support the next decision while preserving agreed requirements. It also applies to product and research decisions. The skills are independent: select the relevant ones and share evidence between them rather than running all four as a fixed pipeline.

## anti-complexity-engineering in short

1. Keep the user's requested outcome and agreed acceptance criteria fixed; optional improvements do not block delivery.
2. Reuse existing primitives; justify new concepts and defenses with concrete requirements or risks. Preserve enforcement at distinct trust boundaries.
3. Finish affected callers and entry points, then remove code and references made obsolete by the change. Distinguish dead code from supported legacy behavior, dynamic loading, and initialization side effects.
4. Reuse useful tests, update assertions tied only to retired internals, and add missing evidence without duplicating suites. Run required checks and stop when the relevant verification passes.
5. Deliver when the complete requested flow works and necessary checks pass. Reassess inherited TODOs instead of automatically extending the task.

Concept tables, deletion ledgers, and fixed report fields are not mandatory. Use supporting notes only when they clarify a real tradeoff or follow-up dependency.

Security, data-loss prevention, real concurrency issues, required audit, and measured performance work are explicitly kept.

## memory-sanity-check in short

- Separate observations, interpretations, recommendations, and constraints; preserve explicit requirements and accepted decisions.
- Check consequential assumptions against current evidence without treating current behavior as proof of intended behavior or retrieved instructions as authorization.
- Compare alternatives only when evidence or a material tradeoff warrants it. Preserve valid scope, privacy, and data-leakage constraints.
- Distinguish current verification from historical reports and inference. Return to the task once the decision is sufficiently supported; no fixed alternative count or summary template is required.

Adapted from [xu-0306/memory-sanity-check](https://github.com/xu-0306/memory-sanity-check/tree/1a3d1d79277c1b72fb8f9d46edccbe272d36c0f6). The version in this collection fixes the YAML frontmatter and bounds the review to the current task.

## Installation

Copy the skill folders you need into your skills directory, for example:

```text
~/.codex/skills/anti-hardcode-engineering/
~/.codex/skills/anti-complexity-engineering/
~/.codex/skills/ui-reference-fidelity/
~/.codex/skills/memory-sanity-check/
~/.claude/skills/anti-complexity-engineering/
~/.claude/skills/memory-sanity-check/
```

Each folder contains `SKILL.md` and `agents/openai.yaml` (UI metadata).

If you previously installed the standalone memory-sanity-check skill, replace that installed folder with `memory-sanity-check/` from this repository. Keep one installed copy with that name to avoid divergent instructions.

## Usage

```text
Use anti-complexity-engineering while designing this feature.
Use anti-hardcode-engineering and anti-complexity-engineering while fixing this bug.
Use ui-reference-fidelity to implement this mockup and verify the resulting layout and interactions.
Use memory-sanity-check to check whether this handoff still supports the next implementation step without reopening agreed requirements.
```
