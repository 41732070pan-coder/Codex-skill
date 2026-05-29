# Quality Gates

Use these checks before finalizing skill changes.

| Gate | Applies to | Check | Command |
| --- | --- | --- | --- |
| Repository skill validation | All skill structure or inventory changes | Front matter, required sections, README inventory, registry inventory, registry columns, and asset manifests are consistent. | `python skills/meta-skill/scripts/validate_skills.py` |
| Whitespace | All changes | No trailing whitespace or conflict markers. | `git diff --check` |
| Naming consistency | Skill rename/addition | Directory, front matter `name`, README, registry, and examples use the same name. | `python skills/meta-skill/scripts/validate_skills.py` / `rg` |
| Required sections | All skills | `SKILL.md` has purpose, triggers/non-triggers, workflow, inputs/outputs, resources, extension, and quality gate. | `python skills/meta-skill/scripts/validate_skills.py` |
| Reference boundary | Skills with references | `SKILL.md` links references and states when to load them. | Manual |
| Registry boundary | Multi-strategy skills | Strategy/provider/mode choices are in a registry. | Manual |
| Template boundary | Extensible skill families | Future implementations have a template. | Manual |
| Asset provenance | Skills with assets | Assets have owner, role, provenance, allowed use, and forbidden use. | `python skills/meta-skill/scripts/validate_skills.py` / Manual |
| README scope | Repository README | README lists skills and functions without duplicating internal manuals. | Manual |

## Rename-Specific Checklist

- Move the directory to `skills/<new-name>/`.
- Update `SKILL.md` front matter `name` and visible title.
- Update `agents/openai.yaml` display metadata and default prompt.
- Update README and `references/skill_registry.md`.
- Search for the old name and either update it or keep it only as historical context when intentional.
- Run `python skills/meta-skill/scripts/validate_skills.py` and `git diff --check`.
