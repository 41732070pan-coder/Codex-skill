# Registry Contract

Use this contract when a skill needs a repository inventory, implementation family registry, provider registry, strategy registry, asset registry, or generated human-readable catalog.

## Purpose

Registries make discovery deterministic. A registry is the concise metadata layer that lets an agent choose what to load without reading every concrete implementation.

## Source Of Truth

| Registry scale | Source-of-truth rule |
| --- | --- |
| Small, stable, human-maintained list | Markdown table is acceptable when a validator can parse it. |
| Growing or user-selectable implementation family | Prefer JSON or YAML as the machine-readable source of truth. |
| Large family, generated catalog, or CI validation | Machine-readable registry plus schema is required; Markdown should be generated or treated as a summary. |

If both machine-readable and Markdown registries exist, the machine-readable registry owns data and the Markdown file is a human-facing mirror.

## Registry Entry Requirements

Every registry should define an entry shape. For implementation families, entries should include at least:

- `id` or `skillName`
- `path` or `implementationPath`
- `status`
- `summary` or `function`
- discovery cues such as aliases, trigger cues, domain cues, medium cues, provider cues, or mode cues
- overlap or ambiguity risks when multiple entries can match the same request

## Schema Rules

Machine-readable registries should have a schema or equivalent validation rules. The validator should check:

- required fields exist
- ids are unique
- aliases or cues do not create unhandled ambiguity
- referenced files and directories exist
- deprecated entries are not selected implicitly
- asset roots have manifests when assets exist
- generated Markdown summaries, if any, are in sync or clearly marked as generated

## Agent Loading Rules

- Use registries to discover candidates and resolve names, aliases, domains, media, providers, or modes.
- Do not use registries as a place for long implementation instructions.
- Do not require agents to read all concrete implementation files to answer “what options exist?”
- When a registry points to implementation files, load only the selected path after resolution or during scoped maintenance.

## Markdown Registry Guidance

Markdown registries should stay concise and table-shaped. They are appropriate for human scanning and short inventories, but should not become large manuals.

A Markdown registry should include:

```markdown
| Id | Path | Status | Summary | Cues | Notes |
| --- | --- | --- | --- | --- | --- |
```

A Markdown registry should avoid:

- long implementation-specific instructions
- complete asset file catalogs
- duplicate content already owned by implementation files
- hidden selection rules buried outside structured columns

## Quality Checklist

Before finalizing registry changes:

- The registry has a declared entry shape.
- The registry is the correct format for its expected scale.
- A validator can read the registry or the registry explicitly documents why validation is manual.
- All referenced implementation, asset, or provider paths exist.
- `SKILL.md` uses the registry through script interfaces instead of duplicating the registry.
