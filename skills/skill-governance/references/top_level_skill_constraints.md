# Top-Level Skill Constraints

This file is the repository-level constraint reference for engineering Codex skills. It exists so future skills can be added consistently instead of becoming isolated prompt folders.

## Architectural Invariants

| Invariant | Rule | Rationale |
| --- | --- | --- |
| Skill root | All maintained skills live under `skills/<skill-name>/`. | Keeps future skill families discoverable and avoids root clutter. |
| Orchestration boundary | `SKILL.md` owns workflow, triggers, and invariant rules. | Codex can start from one file without loading the whole repository. |
| Reference boundary | `references/` owns contracts, registries, templates, and domain details. | Enables progressive disclosure and controlled context loading. |
| Asset boundary | `assets/` is skill-owned; no cross-skill asset reuse unless mediated by a documented shared provider. | Prevents accidental brand, license, or semantic leakage. |
| Registry boundary | Multiple strategies/providers require an explicit registry. | Avoids hidden selection logic in prose. |
| Quality boundary | Every skill declares self-check criteria and runnable checks when available. | Makes outputs reviewable and repeatable. |

## Canonical Skill Lifecycle

```text
idea
  -> draft contract
  -> prototype references/templates
  -> register strategies/providers
  -> add examples/assets if needed
  -> self-check and README inventory update
  -> stable skill
  -> deprecate or migrate when replaced
```

## Data-Structure Checklist

When adding a skill, prefer explicit structures:

- Use a **table** for registries, providers, supported modes, assets, and quality gates.
- Use an **enum** for finite states, modes, output types, and lifecycle status.
- Use a **map/dictionary** for token systems, aliases, role mappings, and strategy lookup.
- Use a **state machine** for multi-step user workflows.
- Use a **dependency graph** for references or assets that must be loaded in order.
- Use a **template** for future implementations in the same family.

## Default New-Skill Template

A new skill should answer these questions before detailed prose is added:

1. What user request should trigger this skill?
2. What user request should not trigger this skill?
3. What normalized input object does the skill operate on?
4. What output artifacts does it produce?
5. What strategies/providers/templates might be added later?
6. What references should be loaded only on demand?
7. What assets or external resources are owned by the skill?
8. What checks prove the output is acceptable?
