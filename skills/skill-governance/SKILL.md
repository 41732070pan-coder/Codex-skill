---
name: skill-governance
description: Meta-skill for engineering, reviewing, and evolving Codex skills in this repository. Use when Codex needs to add a new skill, restructure skill directories, define skill contracts, audit skill quality, or translate a fuzzy capability idea into a maintainable skill with design-pattern, data-structure, registry, lifecycle, and quality-gate discipline.
---

# Skill Governance

Use this skill as the top-level engineering constraint for every skill in this repository. It is the "skill for building skills": before adding or changing a concrete skill, model the skill as a small software system with explicit interfaces, state, registries, assets, tests, and quality gates.

## Core Philosophy

A skill is not just a prompt file. Treat each skill as an engineered capability module:

- **Interface first**: define trigger conditions, inputs, outputs, constraints, and failure modes before writing long instructions.
- **Separation of concerns**: keep orchestration in `SKILL.md`; move reusable contracts, registries, templates, and domain references into `references/`.
- **Design patterns over ad hoc branches**: use Template Method, Strategy, Registry, Adapter, Factory, Composite, State Machine, and Quality Gate patterns when they clarify extension points.
- **Data structures over prose sprawl**: model skill metadata as tables, maps, enums, schemas, checklists, state transitions, and dependency graphs.
- **Substitutability**: skills in the same family should expose comparable sections so future workflows can swap or compose them safely.
- **Minimal context loading**: organize references so Codex can load only the files relevant to the current request.
- **Asset provenance**: every bundled asset must have an owner, role, license/provenance note, and usage constraints.
- **Quality is executable where possible**: document lint, validation, snapshot, or self-check commands when a skill has runnable artifacts.

## Repository-Level Skill Contract

Every skill directory under `skills/<skill-name>/` should follow this shape unless there is a documented reason not to:

```text
skills/<skill-name>/
├── SKILL.md
├── agents/
│   └── openai.yaml              # optional display metadata
├── references/
│   ├── *_contract.md            # interfaces and data shapes
│   ├── *_registry.md            # concrete implementations or providers
│   ├── *_template.md            # template for future extensions
│   └── *.md                     # domain references loaded on demand
├── assets/                      # optional, skill-owned only
│   └── ...
└── examples/                    # optional examples or fixtures
```

Required sections for `SKILL.md`:

1. YAML front matter with `name` and `description`.
2. Purpose and trigger rules.
3. Programming model or workflow.
4. Required interfaces / data shapes.
5. Extension rules.
6. Quality gate / self-check.
7. Asset and external dependency policy, if applicable.

## Skill Data Model

Use this conceptual model when creating or refactoring skills:

```ts
type SkillStatus = "draft" | "experimental" | "stable" | "deprecated";
type SkillArtifactKind = "instruction" | "reference" | "template" | "asset" | "example" | "validator";

interface SkillModule {
  name: string;
  status: SkillStatus;
  purpose: string;
  triggers: string[];
  inputs: Record<string, unknown>;
  outputs: Record<string, unknown>;
  constraints: string[];
  references: SkillArtifact[];
  assets: SkillAsset[];
  extensionPoints: ExtensionPoint[];
  qualityGates: QualityGate[];
}

interface SkillArtifact {
  path: string;
  kind: SkillArtifactKind;
  loadWhen: string;
  ownsDecisions: string[];
}

interface SkillAsset {
  path: string;
  role: string;
  provenance: string;
  allowedUse: string[];
  forbiddenUse: string[];
}
```

## Design Pattern Guidance

- **Template Method**: put invariant workflow in `SKILL.md`; delegate variable decisions to reference files.
- **Strategy**: represent concrete styles, learning methods, tool providers, or output modes as interchangeable strategy files.
- **Registry**: maintain `*_registry.md` when a skill has multiple strategies, providers, or templates.
- **Factory**: define how a request becomes a normalized work item before selecting strategies.
- **Adapter**: isolate external APIs, file formats, model quirks, or platform-specific output rules.
- **Composite**: use when a skill orchestrates nested modules, such as a learning plan made from lessons, drills, reviews, and assessments.
- **State Machine**: use for workflows with explicit phases, such as diagnose → plan → practice → review → revise.
- **Quality Gate**: define pass/fail checks before returning final artifacts.

## Adding A New Skill

1. Create `skills/<skill-name>/SKILL.md` from the required section list above.
2. Decide whether the skill is a single module or a family of strategies.
3. If it is a family, add a contract file, registry file, and template file under `references/`.
4. Add `agents/openai.yaml` when the skill should appear with custom display metadata.
5. Add assets only under that skill's own `assets/` directory and document their usage constraints.
6. Update the repository `README.md` skill inventory and directory tree.
7. Run available checks; at minimum run `git diff --check` for documentation-only changes.

## Self-Check

Before finishing a skill change, verify:

- The new or changed skill has a clear trigger boundary and does not silently overlap another skill.
- The directory layout follows `skills/<skill-name>/...`.
- Extension points are represented as explicit contracts, registries, templates, tables, or schemas.
- Assets are owned by exactly one skill and have documented usage rules.
- The README inventory is accurate.
- No one-off instruction belongs in a reusable contract or governance rule instead.
