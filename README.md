# Engineering Guardrails

Skills for coding agents (Codex, Claude Code, and other agents that load `SKILL.md` folders) that keep changes from going wrong in two opposite directions.

| Skill | Prevents | Use when |
|---|---|---|
| [anti-hardcode-engineering](anti-hardcode-engineering/) | fixes that are too narrow: keyword lists, copied examples, brittle selectors, provider strings | fixing a specific open-world bug at one boundary |
| [anti-complexity-engineering](anti-complexity-engineering/) | unnecessary entities and layers, parallel lifecycles, scope drift, and excessive planning or completion gates | designing or reviewing structural changes, or fixes that add wrappers |

Use either skill when relevant, or both when a fix needs them. anti-hardcode-engineering chooses the right abstraction for one bug; anti-complexity-engineering keeps that abstraction and the surrounding workflow proportional to the requested outcome.

## anti-complexity-engineering in short

1. Keep the user's requested outcome and agreed acceptance criteria fixed; optional improvements do not block delivery.
2. Reuse existing primitives and justify new concepts with concrete requirements. Consult references when the architectural choice needs them.
3. Fix root causes and remove redundant paths when safe, without forcing unrelated deletions or rewrites.
4. Keep planning and verification proportional. Tests verify requirements rather than inventing them.
5. Deliver when the complete requested flow works and necessary checks pass. Reassess inherited TODOs instead of automatically extending the task.

Concept tables, deletion ledgers, and fixed report fields are not mandatory. Use supporting notes only when they clarify a real tradeoff or follow-up dependency.

Security, data-loss prevention, real concurrency issues, required audit, and measured performance work are explicitly kept.

## Installation

Copy one or both skill folders into your skills directory, for example:

```text
~/.codex/skills/anti-hardcode-engineering/
~/.codex/skills/anti-complexity-engineering/
~/.claude/skills/anti-complexity-engineering/
```

Each folder contains `SKILL.md` and `agents/openai.yaml` (UI metadata).

## Usage

```text
Use anti-complexity-engineering while designing this feature.
Use anti-hardcode-engineering and anti-complexity-engineering while fixing this bug.
```
