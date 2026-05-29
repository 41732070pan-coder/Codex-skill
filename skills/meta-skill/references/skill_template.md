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
3. <Execute the skill-specific process.>
4. <Validate and revise.>

## Inputs And Outputs

| Contract | Details |
| --- | --- |
| Required inputs | <files, prompt fields, assets, URLs, or none> |
| Optional inputs | <optional context> |
| Outputs | <artifact types> |
| Failure modes | <when to stop, ask, or decline> |

## References

| Reference | Load when |
| --- | --- |
| `references/<name>.md` | <condition> |

## Resources

- Assets: `<none>` or `assets/<...>` with manifest/provenance.
- External dependencies: `<none>` or list with constraints.
- Shared providers: `<none>` or documented provider paths.

## Extension Points

| Extension | Pattern | File |
| --- | --- | --- |
| <strategy/provider/template> | <registry/strategy/etc.> | <path> |

## Quality Gate

Before finishing, verify:

- Trigger boundary is clear.
- Output matches the requested artifact type.
- References were loaded only as needed.
- Assets and external dependencies follow policy.
- Runnable checks passed, if available.
```
