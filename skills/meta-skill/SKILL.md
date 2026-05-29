---
name: meta-skill
description: Meta-skill for designing, reviewing, refactoring, and governing Codex skills in this repository. Use when Codex needs to add a new skill, rename or restructure a skill, define skill contracts, create registries or templates, audit skill quality, or turn a fuzzy capability idea into a maintainable skill module with lifecycle, resource, and quality-gate discipline.
---

# Meta Skill

## Purpose

Use this skill as the repository-level engineering guide for building and maintaining other skills. Treat every skill as a small capability module with a clear trigger boundary, normalized inputs, outputs, references, assets, extension points, lifecycle status, and quality gates.

## Triggers And Non-Triggers

| Type | Cues |
| --- | --- |
| Trigger | Add, rename, split, merge, deprecate, or refactor a skill. |
| Trigger | Convert a fuzzy capability idea into a concrete skill design. |
| Trigger | Define or review skill contracts, registries, templates, providers, assets, examples, or validators. |
| Trigger | Audit whether an existing skill is maintainable, discoverable, non-overlapping, and safe to extend. |
| Non-trigger | Execute the domain work handled by a concrete skill without changing that skill's structure or governance. |
| Ask if ambiguous | The request sounds like both a one-off prompt and a maintainable skill; clarify whether the user wants a reusable repository module. |

## Core Principles

- **Interface first**: define triggers, non-triggers, inputs, outputs, constraints, and failure modes before adding long instructions.
- **Small SKILL.md, loaded references**: keep orchestration, triggers, workflow, and invariants in `SKILL.md`; move contracts, registries, templates, and domain details into `references/`.
- **Explicit structures over prose sprawl**: use tables, enums, maps, schemas, lifecycle states, checklists, state machines, and dependency graphs.
- **Patterns over ad hoc branches**: prefer Template Method, Strategy, Registry, Factory, Adapter, Composite, State Machine, and Quality Gate when they clarify extension points.
- **Substitutability**: skills in the same family should expose comparable sections and data shapes.
- **Progressive disclosure**: organize references so Codex loads only what the current request needs.
- **Owned resources**: assets belong to one skill or to an explicitly documented shared provider; each asset needs role, provenance, allowed use, and forbidden use.
- **Executable quality when possible**: document validation, lint, snapshot, example, or self-check commands when runnable artifacts exist.

## Workflow

1. **Classify the change**: new skill, rename, refactor, family expansion, asset addition, registry update, validation update, or deprecation.
2. **Normalize the capability**: define user goal, triggers, non-triggers, expected inputs, expected outputs, constraints, lifecycle status, and risk areas.
3. **Choose the module shape**:
   - Single skill: one `SKILL.md` plus optional references.
   - Skill family: add contract, registry, template, and strategy/provider reference files.
   - Resource-heavy skill: add asset manifests, examples, or validators.
4. **Load only the needed references**: use the Reference Load Map instead of reading every reference by default.
5. **Update repository documentation**: keep `README.md` concise; it should list skills and functions, not duplicate internal skill manuals.
6. **Validate**: run available checks. For documentation-only changes, run at least `git diff --check`; for repository-level skill integrity, run `python skills/meta-skill/scripts/validate_skills.py`.

## Inputs And Outputs

| Contract | Details |
| --- | --- |
| Required inputs | A user request that changes, reviews, audits, or formalizes one or more skills. |
| Optional inputs | Existing skill folders, desired lifecycle status, examples, assets, external constraints, or validation expectations. |
| Normalized shape | `{ taskType, affectedSkills, triggers, nonTriggers, inputs, outputs, resources, extensionPoints, qualityGates }`. |
| Outputs | Skill plans, revised `SKILL.md` files, contracts, registries, templates, quality reports, README updates, or validation scripts. |
| Failure modes | Stop or ask when the request is only a one-off prompt, when asset provenance is unclear, or when a proposed skill overlaps an existing skill without a clear boundary. |

## Default Skill Layout

Every maintained skill should normally live under `skills/<skill-name>/`:

```text
skills/<skill-name>/
├── SKILL.md                       # required: trigger, workflow, invariants
├── agents/openai.yaml             # recommended display metadata
├── references/                    # optional on-demand context
│   ├── *_contract.md              # interfaces and data shapes
│   ├── *_registry.md              # strategies, providers, modes, templates
│   ├── *_template.md              # future implementation skeletons
│   └── *.md                       # domain references
├── assets/                        # optional skill-owned assets
├── examples/                      # optional examples or fixtures
└── scripts/                       # optional validators or deterministic helpers
```

The authoritative required-section contract lives in `references/governance_contract.md`; this layout only describes the usual file placement. Keep `SKILL.md` focused on orchestration and load details from `references/` according to the Reference Load Map below.

## References

Load references progressively. `references/governance_contract.md` is the single source of truth for required sections, lifecycle/status fields, data shapes, and review criteria; other references should not redefine those rules.

| Task type | Load references | Skip when |
| --- | --- | --- |
| Add a new maintained skill | `top_level_skill_constraints.md`, `governance_contract.md`, `skill_template.md`, `skill_registry.md`, `quality_gates.md` | The request is a one-off/simple prompt that should not become a maintained skill. |
| Rename, move, deprecate, split, or merge a skill | `top_level_skill_constraints.md`, `skill_registry.md`, `quality_gates.md`; add `governance_contract.md` if contracts change | The task only executes an existing domain skill without changing its structure. |
| Review or audit an existing skill | `top_level_skill_constraints.md`, `governance_contract.md`, `quality_gates.md`, `skill_registry.md` | The user asks only for domain output, not governance feedback. |
| Add strategies, providers, templates, examples, or validators | `governance_contract.md`, `skill_template.md`, `quality_gates.md`; add `skill_registry.md` only if repository-level discovery changes | The change is internal wording with no new extension point. |
| Add or reorganize skill assets | `top_level_skill_constraints.md`, `governance_contract.md`, `quality_gates.md` | The active skill has no bundled or shared assets. |
| Final review before commit or PR | `quality_gates.md`; add `skill_registry.md` when inventory/status changed | No files changed. |

## Resources

| Resource | Role | Load or run when |
| --- | --- | --- |
| `references/governance_contract.md` | Authoritative contract for required sections, lifecycle/status fields, data shapes, and review criteria. | Designing or reviewing any maintained skill. |
| `references/top_level_skill_constraints.md` | Repository-wide invariants for naming, layout, references, assets, README scope, and quality boundaries. | Adding, renaming, restructuring, or auditing skills. |
| `references/skill_template.md` | Copyable skeleton for new maintained skills. | Creating a new skill or standardizing an existing skill. |
| `references/skill_registry.md` | Repository-level inventory for maintained skills. | Adding, removing, renaming, deprecating, or reviewing skill discovery. |
| `references/quality_gates.md` | Manual and executable quality checks. | Before finalizing any skill change. |
| `scripts/validate_skills.py` | Lightweight repository skill validator with no third-party dependencies. | Before commit or PR, especially after changing skill structure, registries, or README inventory. |

The `meta-skill` owns no reusable visual or binary assets. Do not add assets to it unless they support repository governance and include provenance, allowed-use, and forbidden-use documentation.

## Extension Points

| Extension | Pattern | File |
| --- | --- | --- |
| New repository skill | Template Method | `references/skill_template.md` |
| Skill metadata and lifecycle | Contract | `references/governance_contract.md` |
| Repository skill discovery | Registry | `references/skill_registry.md` |
| Quality enforcement | Quality Gate | `references/quality_gates.md`, `scripts/validate_skills.py` |
| Repository invariants | Policy reference | `references/top_level_skill_constraints.md` |

Before adding detailed prose, answer these questions:

| Question | Required outcome |
| --- | --- |
| What should trigger this skill? | Clear trigger phrases, domains, or task cues. |
| What should not trigger it? | Non-trigger and overlap boundaries. |
| What normalized input does it use? | A request object, table, or field list. |
| What outputs does it produce? | Artifact types and success criteria. |
| What can vary later? | Strategies, providers, templates, modes, or adapters. |
| What references load on demand? | Reference list with `loadWhen` guidance. |
| What resources does it own? | Asset/external dependency policy and provenance. |
| What proves quality? | Self-checks and runnable validations where possible. |

## Quality Gate

Before finishing a skill change, verify:

- The skill name, directory, front matter, README inventory, and registry entry agree.
- Trigger and non-trigger boundaries are explicit and do not silently overlap another skill.
- `SKILL.md` remains the orchestration layer; reusable details live in `references/`.
- Multi-strategy or multi-provider behavior is represented by a registry, not hidden prose branches.
- Assets are skill-owned or shared-provider-owned with provenance and usage constraints.
- Extension points are represented by contracts, registries, templates, tables, or schemas.
- The README stays repository-level and avoids duplicating detailed internal skill documentation.
- Run `python skills/meta-skill/scripts/validate_skills.py` and `git diff --check`; record any failures or environment limitations.
