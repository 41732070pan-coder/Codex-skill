# Skill Template

Copy this shape when creating a new maintained skill. This template is derived from `governance_contract.md`, which remains the authoritative source for required sections and data shapes. Remove sections only when they are explicitly not applicable.

```markdown
---
name: <skill-name>
description: <what this skill does, when to use it, and key trigger cues>
---

# <Skill Display Name>

## Purpose

<Describe the capability and the user requests that should trigger it.>

## Triggers And Non-Triggers

| Type | Cues |
| --- | --- |
| Trigger | <phrases, domains, task types> |
| Non-trigger | <nearby tasks handled elsewhere or out of scope> |
| Ask if ambiguous | <when to ask before proceeding> |

## Workflow

1. <Normalize request.>
2. <Load required references only when needed.>
3. <If this skill has an implementation family, use the list/resolve/get scripts before loading implementation content.>
4. <Execute the skill-specific process.>
5. <Validate and revise.>

## Inputs And Outputs

| Contract | Details |
| --- | --- |
| Required inputs | <files, prompt fields, assets, URLs, or none> |
| Optional inputs | <optional context> |
| Normalized shape | <request object or field list> |
| Outputs | <artifact types> |
| Failure modes | <when to stop, ask, or decline> |

## References

Load references progressively; do not read every reference by default.

| Reference | Load when |
| --- | --- |
| `references/<name>.md` | <condition> |

## Resources

- Assets: `<none>` or `assets/<...>` with manifest/provenance.
- External dependencies: `<none>` or list with constraints.
- Shared providers: `<none>` or documented provider paths.
- Discovery resources: `<none>` or registries/list/resolve scripts.
- Implementation resources: `<none>` or selected implementation paths loaded only after resolution or during maintenance.

## Implementation Families

Use this section only when the skill owns multiple interchangeable implementations.

| Family | Registry | List | Resolve | Get / Materialize | Validate |
| --- | --- | --- | --- | --- | --- |
| `<family-name>` | `<path>` | `<command>` | `<command>` | `<command>` | `<command>` |

Normal-use rule: do not browse all implementation files; discover through registry/scripts and load one selected implementation.

## Extension Points

| Extension | Pattern | File |
| --- | --- | --- |
| <strategy/provider/template/family> | <registry/strategy/etc.> | <path> |

## Quality Gate

Before finishing, verify:

- Trigger boundary is clear.
- Output matches the requested artifact type.
- References were loaded only as needed.
- Implementation families use list/resolve/get scripts when applicable.
- Assets and external dependencies follow policy.
- Runnable checks passed, if available.
```
