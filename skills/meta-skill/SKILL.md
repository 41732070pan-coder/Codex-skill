---
name: meta-skill
description: Meta-skill for designing, reviewing, refactoring, and governing Codex skills in this repository. Use when Codex needs to add a new skill, rename or restructure a skill, define skill contracts, create registries or templates, audit skill quality, create implementation-family dispatch protocols, or turn a fuzzy capability idea into a maintainable skill module with lifecycle, resource, and quality-gate discipline.
---

# Meta Skill

## Purpose

Use this skill as the repository-level engineering guide for building and maintaining other skills. Treat every skill as a small capability module with a clear trigger boundary, normalized inputs, outputs, references, assets, extension points, lifecycle status, and quality gates.

This skill also owns the repository standard for **implementation families**: any skill-internal collection of interchangeable styles, providers, strategies, adapters, modes, templates, renderers, or other concrete implementations that can grow beyond a few entries.

## Triggers And Non-Triggers

| Type | Cues |
| --- | --- |
| Trigger | Add, rename, split, merge, deprecate, or refactor a skill. |
| Trigger | Convert a fuzzy capability idea into a concrete skill design. |
| Trigger | Define or review skill contracts, registries, templates, providers, assets, examples, validators, or resource access boundaries. |
| Trigger | Audit whether an existing skill is maintainable, discoverable, non-overlapping, safe to extend, and safe to load progressively. |
| Trigger | Add or refactor a multi-implementation family such as visual styles, strategy variants, providers, adapters, modes, or templates. |
| Non-trigger | Execute the domain work handled by a concrete skill without changing that skill's structure or governance. |
| Ask if ambiguous | The request sounds like both a one-off prompt and a maintainable skill; clarify whether the user wants a reusable repository module. |

## Core Principles

- **Interface first**: define triggers, non-triggers, inputs, outputs, constraints, and failure modes before adding long instructions.
- **Small SKILL.md, loaded references**: keep orchestration, triggers, workflow, and invariants in `SKILL.md`; move contracts, registries, templates, domain details, and concrete implementations behind references, registries, scripts, or implementation directories.
- **No implementation fan-out from `SKILL.md`**: `SKILL.md` may describe how to discover and select implementations, but must not become an index of every concrete implementation in a growing family.
- **Upgradeable discovery before implementation loading**: multi-implementation skills start with a concise registry and upgrade to list, resolve, and materialize/get scripts as scale, ambiguity, assets, or validation needs grow.
- **Explicit structures over prose sprawl**: use tables, enums, maps, schemas, lifecycle states, checklists, state machines, and dependency graphs.
- **Patterns over ad hoc branches**: prefer Template Method, Strategy, Registry, Factory, Adapter, Composite, State Machine, and Quality Gate when they clarify extension points.
- **Substitutability**: skills in the same family should expose comparable sections and data shapes.
- **Progressive disclosure**: organize references so Codex loads only what the current request needs.
- **Registry-driven recommendation**: resolve or recommend implementations from declared ids, aliases, cues, summaries, ambiguity policy, and fallback policy; do not rely on implementation-body browsing or unlabeled substitutes.
- **Owned resources**: assets belong to one skill or to an explicitly documented shared provider; each asset needs role, provenance, allowed use, and forbidden use.
- **Executable quality when possible**: document validation, lint, snapshot, example, or self-check commands when runnable artifacts exist.

## Workflow

1. **Classify the change**: new skill, rename, refactor, family expansion, implementation addition, registry update, resource-boundary audit, validation update, asset addition, or deprecation.
2. **Normalize the capability**: define user goal, triggers, non-triggers, expected inputs, expected outputs, constraints, lifecycle status, risk areas, and whether the skill has or will have an implementation family.
3. **Choose the module shape**:
   - Single skill: one `SKILL.md` plus optional references.
   - Governed skill: add contract, registry, template, and validator references.
   - Small implementation family: add a concise, table-shaped registry with stable ids, implementation paths, status, aliases/cues, ambiguity policy, fallback policy, and selected-only loading.
   - Growing implementation family: preserve the same entry semantics, then add a machine-readable registry, list/resolve/get scripts, implementation template, and boundary validation.
   - Resource-heavy skill: add asset manifests, examples, providers, or deterministic helpers.
4. **Apply the load boundary**:
   - During normal use, load `SKILL.md` first, then only the references in the Reference Load Map.
   - For implementation families, do not inspect all implementation files. Use the family registry or list/resolve/get scripts first.
   - Resolve directly when possible; when resolution is ambiguous or missing, provide available implementation ids and summaries so the LLM can choose the most likely option or recommend a close registered option.
   - Direct implementation reads are maintenance-only and should be scoped to the selected implementation or the files being edited.
5. **Update repository documentation**: keep `README.md` concise; it should list skills and functions, not duplicate internal skill manuals or implementation catalogs.
6. **Validate**: run available checks. For documentation-only changes, run at least `git diff --check`; for repository-level skill integrity, run `python skills/meta-skill/scripts/validate_skills.py`; for load-boundary work, run `python skills/meta-skill/scripts/validate_skill_boundaries.py`.


## Normal Use Loading Rule

For a skill with an implementation family, normal use must follow this minimum path regardless of whether the family is small or fully scripted:

1. Read `SKILL.md` for triggers, workflow, and loading policy.
2. Use the concise registry or list/resolve scripts to discover candidates without reading implementation bodies.
3. Resolve directly when declared ids, aliases, cues, and ambiguity policy identify one implementation.
4. If resolution is ambiguous or missing, provide the LLM with available implementation ids, summaries, and match reasons so it can choose the most likely intended implementation or recommend a close registered option.
5. Label recommendations as recommendations rather than exact matches; if no useful registered option exists, offer a skill-extension path.
6. Load only the resolved or explicitly recommended implementation through its path or get/materialize command.
7. Do not read sibling implementation bodies unless the task is comparison, migration, validation authoring, or explicit audit.

This skill defines repository design and validation policy. It does not provide runtime filesystem access control; runtime enforcement belongs to the agent runner, tool gateway, CI, or audit layer.

## Inputs And Outputs

| Contract | Details |
| --- | --- |
| Required inputs | A user request that changes, reviews, audits, formalizes, or governs one or more skills. |
| Optional inputs | Existing skill folders, desired lifecycle status, examples, assets, external constraints, implementation families, registry formats, or validation expectations. |
| Normalized shape | `{ taskType, affectedSkills, triggers, nonTriggers, inputs, outputs, resources, extensionPoints, implementationFamilies, loadPolicy, qualityGates }`. |
| Outputs | Skill plans, revised `SKILL.md` files, contracts, registries, templates, quality reports, README updates, validators, or implementation-family dispatch protocols. |
| Failure modes | Stop or ask when the request is only a one-off prompt, when asset provenance is unclear, when a proposed skill overlaps an existing skill without a clear boundary, or when a proposed family cannot expose deterministic discovery. |

## Default Skill Layout

Every maintained skill should normally live under `skills/<skill-name>/`:

```text
skills/<skill-name>/
├── SKILL.md                       # required: trigger, workflow, invariants
├── agents/openai.yaml             # recommended display metadata
├── references/                    # optional on-demand context
│   ├── *_contract.md              # interfaces and data shapes
│   ├── *_registry.md              # human-readable registries or generated summaries
│   ├── *_template.md              # future implementation skeletons
│   └── *.md                       # domain references
├── registry/                      # optional machine-readable registries and schemas
├── implementations/               # optional concrete implementations for growing families
├── assets/                        # optional skill-owned assets
├── examples/                      # optional examples or fixtures
└── scripts/                       # optional validators or deterministic helpers
```

The authoritative required-section contract lives in `references/governance_contract.md`; this layout only describes the usual file placement. Keep `SKILL.md` focused on orchestration and load details from `references/` according to the Reference Load Map below.

## Implementation Family Standard

Use an implementation family when one skill owns multiple interchangeable concrete implementations such as styles, providers, strategies, adapters, modes, or templates.

| Requirement | Rule |
| --- | --- |
| Family contract | Define selection, loading, data shape, and maintenance rules in a family contract or in `references/implementation_family_contract.md`. |
| Registry | Put implementation metadata in a registry; a small stable family may use a concise Markdown table, while a growing or ambiguity-prone family should move the source of truth to machine-readable JSON/YAML. |
| Upgrade-compatible fields | Keep stable ids, implementation paths, status, summaries, aliases/cues, ambiguity policy, and fallback policy from the first small-family version so later scripts can reuse the same semantics. |
| Discovery scripts | Expose list and resolve scripts when the family grows, has ambiguous cues, owns assets, needs CI validation, or cannot be reliably resolved from a short table. |
| Materialization script | Expose a get/materialize script for growing families; it returns only the selected implementation, ideally filtered by medium, mode, section, or task. |
| `SKILL.md` boundary | Do not list every concrete implementation in `SKILL.md` once a family is expected to grow. Describe the registry and dispatch interface instead. |
| Resolution semantics | Use `resolved`, `ambiguous`, or `unresolved` outcomes. Ambiguous or unresolved cases should return available candidates and summaries so the LLM can choose or recommend a registered implementation without pretending it was an exact match. |
| Maintenance exception | Directly open implementation files only when adding, editing, debugging, or reviewing the specific implementation involved. |

## References

Load references progressively. `references/governance_contract.md` is the single source of truth for required sections, lifecycle/status fields, data shapes, and review criteria; other references should not redefine those rules.

| Task type | Load references | Skip when |
| --- | --- | --- |
| Add a new maintained skill | `top_level_skill_constraints.md`, `governance_contract.md`, `skill_template.md`, `skill_registry.md`, `quality_gates.md` | The request is a one-off/simple prompt that should not become a maintained skill. |
| Rename, move, deprecate, split, or merge a skill | `top_level_skill_constraints.md`, `skill_registry.md`, `quality_gates.md`; add `governance_contract.md` if contracts change | The task only executes an existing domain skill without changing its structure. |
| Review or audit an existing skill | `top_level_skill_constraints.md`, `governance_contract.md`, `resource_access_contract.md`, `quality_gates.md`, `skill_registry.md` | The user asks only for domain output, not governance feedback. |
| Add or refactor an implementation family | `implementation_family_contract.md`, `registry_contract.md`, `implementation_family_template.md`, `resource_access_contract.md`, `quality_gates.md` | The skill has only one concrete behavior and no expected family growth. |
| Add strategies, providers, templates, examples, or validators | `governance_contract.md`, `implementation_family_contract.md` when multiple implementations exist, `skill_template.md`, `quality_gates.md`; add `skill_registry.md` only if repository-level discovery changes | The change is internal wording with no new extension point. |
| Add or reorganize skill assets | `top_level_skill_constraints.md`, `resource_access_contract.md`, `governance_contract.md`, `quality_gates.md` | The active skill has no bundled or shared assets. |
| Audit progressive loading or implementation fan-out | `resource_access_contract.md`, `implementation_family_contract.md`, `registry_contract.md`, `quality_gates.md`; run `scripts/validate_skill_boundaries.py` | No skill exposes references, assets, registries, or implementation families. |
| Final review before commit or PR | `quality_gates.md`; add `skill_registry.md` when inventory/status changed | No files changed. |

## Resources

| Resource | Role | Load or run when |
| --- | --- | --- |
| `references/governance_contract.md` | Authoritative contract for required sections, lifecycle/status fields, data shapes, and review criteria. | Designing or reviewing any maintained skill. |
| `references/implementation_family_contract.md` | Contract for multi-implementation families, dispatch scripts, and normal-use loading boundaries. | Adding or refactoring styles, providers, strategies, adapters, modes, or templates. |
| `references/registry_contract.md` | Registry format, source-of-truth, schema, and generated-document rules. | Designing or validating skill, family, strategy, provider, or asset registries. |
| `references/resource_access_contract.md` | Public, discovery, implementation, asset, generated, and maintenance-only resource classes. | Auditing what an agent may load by default or after resolution. |
| `references/top_level_skill_constraints.md` | Repository-wide invariants for naming, layout, references, assets, README scope, and quality boundaries. | Adding, renaming, restructuring, or auditing skills. |
| `references/skill_template.md` | Copyable skeleton for new maintained skills. | Creating a new skill or standardizing an existing skill. |
| `references/implementation_family_template.md` | Copyable skeleton for a governed implementation family inside a skill. | Creating or standardizing a multi-implementation family. |
| `references/skill_registry.md` | Repository-level inventory for maintained skills. | Adding, removing, renaming, deprecating, or reviewing skill discovery. |
| `references/quality_gates.md` | Manual and executable quality checks. | Before finalizing any skill change. |
| `scripts/validate_skills.py` | Lightweight repository skill validator with no third-party dependencies. | Before commit or PR, especially after changing skill structure, registries, or README inventory. |
| `scripts/validate_skill_boundaries.py` | Static checker for oversized entry files, implementation fan-out, asset fan-out, and missing family dispatch scripts. | After changing `SKILL.md`, references, registry layout, or implementation-family rules. |

The `meta-skill` owns no reusable visual or binary assets. Do not add assets to it unless they support repository governance and include provenance, allowed-use, and forbidden-use documentation.

## Extension Points

| Extension | Pattern | File |
| --- | --- | --- |
| New repository skill | Template Method | `references/skill_template.md` |
| Skill metadata and lifecycle | Contract | `references/governance_contract.md` |
| Multi-implementation family | Strategy + Registry + Factory | `references/implementation_family_contract.md`, `references/implementation_family_template.md` |
| Registry source-of-truth | Registry + Schema | `references/registry_contract.md` |
| Progressive loading/resource access | Access policy | `references/resource_access_contract.md` |
| Repository skill discovery | Registry | `references/skill_registry.md` |
| Quality enforcement | Quality Gate | `references/quality_gates.md`, `scripts/validate_skills.py`, `scripts/validate_skill_boundaries.py` |
| Repository invariants | Policy reference | `references/top_level_skill_constraints.md` |

Before adding detailed prose, answer these questions:

| Question | Required outcome |
| --- | --- |
| What should trigger this skill? | Clear trigger phrases, domains, or task cues. |
| What should not trigger it? | Non-trigger and overlap boundaries. |
| What normalized input does it use? | A request object, table, or field list. |
| What outputs does it produce? | Artifact types and success criteria. |
| What can vary later? | Strategies, providers, templates, modes, adapters, or implementation families. |
| What references load on demand? | Reference list with `loadWhen` guidance. |
| What resources does it own? | Asset/external dependency policy and provenance. |
| How does an agent discover implementations? | Concise registry fields first; add list/resolve scripts when scale, ambiguity, assets, or validation needs justify them. |
| How does an agent resolve ambiguity or missing implementations? | Return candidates and summaries for LLM choice/recommendation, or offer extension when no useful registered option exists; never rely on undeclared model-only aliases. |
| How does an agent load one implementation? | The selected implementation path or a get/materialize script scoped to the selected implementation and task. |
| What proves quality? | Self-checks and runnable validations where possible. |

## Quality Gate

Before finishing a skill change, verify:

- The skill name, directory, front matter, README inventory, and registry entry agree.
- Trigger and non-trigger boundaries are explicit and do not silently overlap another skill.
- `SKILL.md` remains the orchestration layer; reusable details live behind references, registries, scripts, or implementation directories.
- Multi-strategy or multi-provider behavior is represented by a registry, not hidden prose branches.
- Small implementation families use an upgrade-compatible registry entry shape; growing families expose list, resolve, get/materialize, and validation scripts before accumulating concrete implementations.
- Assets are skill-owned or shared-provider-owned with provenance and usage constraints.
- Extension points are represented by contracts, registries, templates, tables, or schemas.
- The README stays repository-level and avoids duplicating detailed internal skill documentation or implementation catalogs.
- Run `python skills/meta-skill/scripts/validate_skills.py`, `python skills/meta-skill/scripts/validate_skill_boundaries.py`, and `git diff --check`; record any failures or environment limitations.
