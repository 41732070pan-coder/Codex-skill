# Implementation Family Template

Copy this shape when a skill needs multiple interchangeable implementations.

```text
skills/<skill-name>/
├── SKILL.md
├── references/
│   ├── <family>_contract.md
│   ├── <family>_template.md
│   └── <family>_registry.md        # optional human-readable summary
├── registry/
│   ├── <family>.json               # preferred source of truth for growing families
│   └── <family>.schema.json        # validation schema or documented equivalent
├── implementations/
│   └── <implementation-id>/
│       ├── implementation.md
│       ├── metadata.json
│       └── assets/
│           └── ASSET_MANIFEST.md
└── scripts/
    ├── list_<family>.py
    ├── resolve_<family>.py
    ├── get_<family>.py
    └── validate_<family>.py
```

## Family Contract Stub

```markdown
# <Family> Contract

## Purpose

<What implementations in this family do and why they are interchangeable.>

## Entry Shape

<Define required metadata fields and implementation sections.>

## Resolution Rules

<Exact id/alias, domain cues, medium cues, priority, ambiguity policy.>

## Loading Rules

<Which script lists, resolves, and materializes one implementation.>

## Asset Rules

<How implementation-owned and shared-provider assets are declared and used.>

## Quality Gate

<Validation command and self-check rules.>
```

## Registry Entry Stub

```json
{
  "id": "<implementation-id>",
  "displayName": "<Human label>",
  "status": "experimental",
  "aliases": [],
  "domainCues": [],
  "mediumCues": [],
  "summary": "<Short option text>",
  "implementationPath": "implementations/<implementation-id>/implementation.md",
  "assetRoot": "none",
  "priority": "explicit-only"
}
```

## Script Behavior Stub

| Command | Behavior |
| --- | --- |
| `python skills/<skill-name>/scripts/list_<family>.py --query "..." --limit 8` | Show candidate ids and summaries only. |
| `python skills/<skill-name>/scripts/resolve_<family>.py --query "..." --medium <medium>` | Return resolved, ambiguous, or unresolved JSON. |
| `python skills/<skill-name>/scripts/get_<family>.py --id <implementation-id> --sections execution` | Return only selected implementation content. |
| `python skills/<skill-name>/scripts/validate_<family>.py` | Validate registry, implementation files, assets, and family contract. |

## `SKILL.md` Stub

```markdown
## <Family> Dispatch

Do not browse all `<family>` implementation files during normal use.

1. If the user names an implementation, run `<resolve command>`.
2. If the user does not name one, run `<list command>` or `<resolve command>` with query cues.
3. If ambiguous, show candidates and ask once.
4. After resolution, run `<get command>` for the selected implementation and task scope.
5. Use only assets declared by the selected implementation.
```

## Quality Checklist

- Family contract exists.
- Registry or documented registry summary exists.
- List, resolve, get/materialize, and validate scripts exist or the family documents why they are not required yet.
- `SKILL.md` exposes dispatch commands, not the full implementation catalog.
- Boundary validator and family validator pass.
