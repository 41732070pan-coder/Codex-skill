# Registry Contract

Use this contract for skill registries, implementation-family registries, provider registries, template registries, strategy maps, asset indexes, or any other discovery surface.

## Purpose

A registry is a concise metadata layer that lets an agent discover, resolve, recommend, and validate options without reading all concrete implementations. It is not an implementation manual.

A registry should also make small families upgradeable. The first registry may be a Markdown table, but its columns should map cleanly to the machine-readable fields a future resolver will consume.

## Source Of Truth

- For small, stable, human-maintained lists, a Markdown table is acceptable when a validator or reviewer can parse the structure.
- For growing or user-selectable implementation families, prefer JSON or YAML as the machine-readable source of truth.
- For large families, generated catalogs, or CI validation, a machine-readable registry plus schema is required; Markdown should be generated or treated as a summary.

If both machine-readable and Markdown registries exist, the machine-readable registry owns data and the Markdown file is a human-facing mirror. Do not hand-maintain the same fields in two places.

## Registry Entry Requirements

Every registry should define an entry shape. For implementation families, entries should include at least:

- `id` or `skillName`
- `path` or `implementationPath`
- `status`
- `summary` or `function`
- discovery cues such as exact aliases, contextual aliases, trigger cues, domain cues, medium cues, provider cues, or mode cues
- negative cues and overlap or ambiguity risks when multiple entries can match the same request
- fallback or recommendation policy for missing or weak matches when the registry drives implementation selection

## Resolution Data Rules

Use registry data to separate confirmed names from weak cues:

| Data | Meaning | Resolver behavior |
| --- | --- | --- |
| `id` | Stable machine identifier. | Exact match resolves unless status blocks use. |
| `exactAliases` / `aliases` | Declared names users may type. | Resolve only when unique or explicitly disambiguated. |
| `contextualAliases` | Short or ambiguous names that need context. | Return candidates and summaries for LLM choice when supporting cues are insufficient. |
| `domainCues`, `mediumCues`, `providerCues`, `modeCues` | Signals that support a match. | Support resolution and candidate ranking; avoid treating a single weak cue as exact proof when ambiguity exists. |
| `negativeCues` | Terms that should block a likely wrong match. | Exclude or demote the candidate. |
| `ambiguityRisks` | Known overlaps and confusion cases. | Return candidates with descriptions so the LLM can choose or recommend without reading implementations. |
| `fallbackPolicy` | What to do when no exact registered implementation matches. | Prefer `recommend-registered` when safe; label recommendations and never pretend they are exact matches. |

Do not encode family-specific alias facts only in resolver code or `SKILL.md`. Keep them in the registry so they can be reviewed, validated, and migrated.

## Schema Rules

Machine-readable registries should have a schema or equivalent validation rules. The validator should check:

- required fields exist
- ids are unique
- exact aliases are unique or explicitly disambiguated
- contextual aliases or cues do not create unhandled ambiguity
- referenced files and directories exist
- deprecated entries are not selected implicitly
- fallback policies are explicit for implementation-selection registries
- asset roots have manifests when assets exist
- generated Markdown summaries, if any, are in sync or clearly marked as generated

## Agent Loading Rules

- Use registries to discover candidates and resolve names, aliases, domains, media, providers, or modes.
- Do not use registries as a place for long implementation instructions.
- Do not require agents to read all concrete implementation files to answer “what options exist?”
- When a registry points to implementation files, load only the selected path after resolution or during scoped maintenance.
- If no registry entry exactly matches, provide available registered options and descriptions for LLM recommendation, or offer an extension path instead of inventing a governed implementation.

## Markdown Registry Guidance

Markdown registries should stay concise and table-shaped. They are appropriate for human scanning and short inventories, but should not become large manuals.

A Markdown implementation-family registry should include upgrade-compatible columns such as:

```markdown
| Id | Path | Status | Summary | Exact aliases | Contextual cues | Ambiguity risks | Fallback |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

A Markdown registry should avoid:

- long implementation-specific instructions
- complete asset file catalogs
- duplicate content already owned by implementation files
- hidden selection rules buried outside structured columns
- data that must later be scraped from prose to become machine-readable

## Upgrade Path

When a Markdown registry outgrows manual scanning or needs scripted validation:

1. Preserve ids, paths, statuses, summaries, aliases/cues, ambiguity risks, and fallback policies.
2. Move those fields into JSON or YAML as the source of truth.
3. Generate or shorten the Markdown registry as a human-facing mirror.
4. Point list/resolve/get/validate scripts at the machine-readable registry.

This path avoids a full redesign because the small-family table already used the large-family field semantics.

## Quality Checklist

Before finalizing registry changes:

- The registry has a declared entry shape.
- The registry is the correct format for its expected scale.
- A validator can read the registry or the registry explicitly documents why validation is manual.
- All referenced implementation, asset, or provider paths exist.
- Ambiguous aliases/cues and recommendation behavior are represented as data, not hidden in prose or model assumptions.
- `SKILL.md` uses the registry through a concise dispatch policy or script interfaces instead of duplicating the registry.
