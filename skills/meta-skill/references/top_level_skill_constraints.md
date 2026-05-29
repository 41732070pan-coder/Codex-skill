# Top-Level Skill Constraints

This file records repository-wide invariants for engineering Codex skills. Use it before adding, renaming, restructuring, or reviewing any skill.

## Architectural Invariants

| Invariant | Rule | Rationale |
| --- | --- | --- |
| Skill root | Maintained skills live under `skills/<skill-name>/`. | Keeps capabilities discoverable and avoids root clutter. |
| Naming | Directory name, front matter `name`, README inventory, and user-facing examples should match. | Prevents trigger confusion and stale references. |
| Orchestration boundary | `SKILL.md` owns triggers, workflow, and invariant rules. | Codex can start from one small file without loading the whole repository. |
| Reference boundary | `references/` owns contracts, registries, templates, and domain details. | Enables progressive disclosure and controlled context loading. |
| Registry boundary | Multiple strategies, providers, modes, or templates require an explicit `*_registry.md`. | Avoids hidden selection logic in prose. |
| Asset boundary | `assets/` is skill-owned; cross-skill reuse requires a documented shared provider. | Prevents brand, license, and semantic leakage. |
| README boundary | `README.md` lists repository skills and their functions; detailed manuals stay inside each skill. | Keeps repository overview short and avoids duplicated drift. |
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

Prefer explicit structures over long prose:

- Use a **table** for registries, providers, supported modes, assets, and quality gates.
- Use an **enum** for finite states, modes, output types, lifecycle status, and risk levels.
- Use a **map/dictionary** for aliases, token systems, role mappings, and strategy lookup.
- Use a **state machine** for multi-step workflows.
- Use a **dependency graph** for references or assets that must be loaded in order.
- Use a **template** for future implementations in the same family.

## Repository Documentation Rule

The root `README.md` should answer:

1. What is this repository for?
2. What skills exist?
3. What does each skill do?
4. Where is each skill located?
5. What is the high-level process for adding another skill?

It should not duplicate each skill's internal contract, concrete strategies, asset policies, or detailed usage manual.
