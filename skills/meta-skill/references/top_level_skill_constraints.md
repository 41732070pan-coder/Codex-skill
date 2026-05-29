# Top-Level Skill Constraints

This file records repository-wide invariants for engineering Codex skills. Use it before adding, renaming, restructuring, or reviewing any skill.

## Architectural Invariants

| Invariant | Rule | Rationale |
| --- | --- | --- |
| Skill root | Maintained skills live under `skills/<skill-name>/`. | Keeps capabilities discoverable and avoids root clutter. |
| Naming | Directory name, front matter `name`, README inventory, and user-facing examples should match. | Prevents trigger confusion and stale references. |
| Orchestration boundary | `SKILL.md` owns triggers, workflow, invariant rules, and dispatch commands. | Codex can start from one small file without loading the whole repository. |
| Reference boundary | `references/` owns contracts, templates, policy references, and concise human-readable registries. | Enables progressive disclosure and controlled context loading. |
| Registry boundary | Multiple strategies, providers, modes, templates, or implementations require an explicit registry. | Avoids hidden selection logic in prose. |
| Implementation boundary | Growing implementation families expose list, resolve, get/materialize, and validate scripts. | Prevents agents from reading every concrete implementation before selecting one. |
| Machine-readable boundary | Large or deterministic registries should use JSON/YAML plus schema or equivalent validation. | Makes discovery stable and scriptable. |
| Asset boundary | `assets/` is skill-owned; cross-skill reuse requires a documented shared provider. | Prevents brand, license, and semantic leakage. |
| README boundary | `README.md` lists repository skills and their functions; detailed manuals and implementation catalogs stay inside each skill. | Keeps repository overview short and avoids duplicated drift. |
| Quality boundary | Every skill declares self-check criteria and runnable checks when available. | Makes outputs reviewable and repeatable. |

## Canonical Skill Lifecycle

```text
idea
  -> draft contract
  -> prototype references/templates
  -> register strategies/providers/implementations
  -> add list/resolve/get scripts for growing families
  -> add examples/assets if needed
  -> self-check and README inventory update
  -> stable skill
  -> deprecate or migrate when replaced
```

## Data-Structure Checklist

Prefer explicit structures over long prose:

- Use a **table** for small registries, providers, supported modes, assets, and quality gates.
- Use **JSON/YAML plus schema** for growing implementation families or deterministic resolution.
- Use an **enum** for finite states, modes, output types, lifecycle status, risk levels, and priority rules.
- Use a **map/dictionary** for aliases, token systems, role mappings, and strategy lookup.
- Use a **state machine** for multi-step workflows.
- Use a **dependency graph** for references or assets that must be loaded in order.
- Use a **template** for future implementations in the same family.
- Use **scripts** for discovery, resolution, materialization, and validation when model behavior should not decide file loading.

## Implementation Family Rule

A skill with a growing set of interchangeable implementations must not require agents to inspect every implementation file during normal use.

The skill should expose:

1. A family contract that defines entry shape, resolution, loading, assets, and quality gates.
2. A registry that contains concise discovery metadata.
3. A list command for available options.
4. A resolve command for names, aliases, cues, media, or modes.
5. A get/materialize command that returns one selected implementation or scoped section.
6. A validation command for registry and implementation conformance.

## Repository Documentation Rule

The root `README.md` should answer:

1. What is this repository for?
2. What skills exist?
3. What does each skill do?
4. Where is each skill located?
5. What is the high-level process for adding another skill?

It should not duplicate each skill's internal contract, concrete strategies, implementation catalogs, asset policies, or detailed usage manual.
