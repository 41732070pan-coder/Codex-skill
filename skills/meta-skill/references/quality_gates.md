# Quality Gates

Use these checks before finalizing skill changes.

| Gate | Applies to | Check | Command |
| --- | --- | --- | --- |
| Remote drift pre-check | Git-backed skill changes before editing | Fetch intended remote and stop when local history is behind or diverged. Configure the remote explicitly if missing. | `python skills/meta-skill/scripts/check_remote_sync.py --fetch` |
| Repository skill validation | All skill structure or inventory changes | Front matter, required sections, README inventory, registry inventory, registry columns, and asset manifests are consistent. | `python skills/meta-skill/scripts/validate_skills.py` |
| Boundary validation | Changes to `SKILL.md`, resource access rules, implementation families, or registries | Entry files stay orchestration-focused; implementation and asset fan-out are limited; growing families expose dispatch scripts. | `python skills/meta-skill/scripts/validate_skill_boundaries.py` |
| Whitespace | All changes | No trailing whitespace or conflict markers. | `git diff --check` |
| Naming consistency | Skill rename/addition | Directory, front matter `name`, README, registry, and examples use the same name. | `python skills/meta-skill/scripts/validate_skills.py` / `rg` |
| Required sections | All skills | `SKILL.md` has purpose, triggers/non-triggers, workflow, inputs/outputs, resources, extension, and quality gate. | `python skills/meta-skill/scripts/validate_skills.py` |
| Reference boundary | Skills with references | `SKILL.md` links references and states when to load them; large details live behind references, registries, or scripts. | `python skills/meta-skill/scripts/validate_skill_boundaries.py` |
| Registry boundary | Multi-strategy or multi-implementation skills | Strategy/provider/mode/implementation choices are in a registry, not hidden prose branches. | `python skills/meta-skill/scripts/validate_skill_boundaries.py` / family validator |
| Implementation-family dispatch | Small and growing implementation families | Small families use upgrade-compatible registry fields and documented script deferral; growing families expose list, resolve, get/materialize, and validate scripts before accumulating implementation files. | `python skills/meta-skill/scripts/validate_skill_boundaries.py` / family validator |
| Template boundary | Extensible skill families | Future implementations have a template or documented skeleton. | `python skills/meta-skill/scripts/validate_skill_boundaries.py` / Manual |
| Asset provenance | Skills with assets | Assets have owner, role, provenance, allowed use, and forbidden use. | `python skills/meta-skill/scripts/validate_skills.py` / Manual |
| README scope | Repository README | README lists skills and functions without duplicating internal manuals or implementation catalogs. | Manual |

## Pre-Edit Checklist

- Before editing a Git-backed workspace, run `python skills/meta-skill/scripts/check_remote_sync.py --fetch` when the intended remote is configured. Stop and report the limitation when no remote URL is available.
- If the branch is behind or diverged, integrate fetched remote changes before editing.

## Rename-Specific Checklist

- Move the directory to `skills/<new-name>/`.
- Update `SKILL.md` front matter `name` and visible title.
- Update `agents/openai.yaml` display metadata and default prompt.
- Update README and `references/skill_registry.md`.
- Search for the old name and either update it or keep it only as historical context when intentional.
- Run `python skills/meta-skill/scripts/validate_skills.py`, `python skills/meta-skill/scripts/validate_skill_boundaries.py`, and `git diff --check`.

## Implementation-Family Checklist

- Define whether the family represents styles, providers, strategies, adapters, modes, templates, or another implementation kind.
- Define registry fields and whether the source of truth is Markdown, JSON, YAML, or generated Markdown.
- Preserve upgrade-compatible fields: id, path, status, summary, aliases/cues, ambiguity risks, and fallback policy.
- Add or document list, resolve, get/materialize, and validate commands; if scripts are deferred for a small family, document why and when to upgrade.
- Keep `SKILL.md` focused on dispatch; do not turn it into a full implementation catalog.
- Ensure list and resolve outputs use concise metadata, not implementation bodies.
- Ensure ambiguous or unresolved requests return candidate ids, summaries, and match reasons for LLM choice/recommendation instead of inventing or blending implementations.
- Ensure get/materialize returns one selected implementation or task-scoped section.
- Add asset manifests for implementation-owned asset roots.
- Run the repository validator, boundary validator, and family-specific validator.
