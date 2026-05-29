# Resource Access Contract

Use this contract to decide what an agent may load by default, what must be discovered through scripts, and what is maintenance-only.

## Purpose

Skill resources should be organized so normal use does not require reading an entire skill directory. The access policy protects context budget, reduces accidental blending between implementations, and makes large skills predictable.

## Resource Classes

| Class | Examples | Normal-use policy |
| --- | --- | --- |
| Public entry | `SKILL.md`, `agents/openai.yaml` | Safe to read when the skill triggers. |
| Governance reference | `references/*_contract.md`, `references/*_template.md`, `references/quality_gates.md` | Load only for design, review, extension, or validation tasks. |
| Discovery resource | `registry/*.json`, concise `*_registry.md`, list/resolve scripts | Safe to use for option discovery and implementation resolution. |
| Implementation resource | `implementations/<id>/`, concrete style/provider/strategy files, detailed domain manuals | Load only after selecting the implementation or during scoped maintenance. |
| Asset resource | `assets/<id>/`, images, SVGs, binary fixtures, manifests | Use only when selected implementation or task declares the asset root. |
| Generated resource | generated catalogs, snapshots, reports | Read when validating generated output or when explicitly referenced. |
| Maintenance-only resource | migration notes, deprecated implementations, raw provider internals | Read only when editing, migrating, debugging, or auditing that scope. |

## Default Loading Policy

1. Start from `SKILL.md`.
2. Use the reference load map for governance and extension tasks.
3. Use discovery scripts or registries before reading implementation resources.
4. Load exactly one selected implementation when executing a family-specific task.
5. Load sibling implementations only for comparison, migration, validation authoring, or explicit user-requested audit.
6. Load assets only through the selected implementation's asset policy and manifest.

## Anti-Patterns

Avoid these patterns in maintained skills:

- `SKILL.md` says to read all files under `references/`, `implementations/`, or `assets/`.
- `SKILL.md` lists dozens of concrete implementations instead of pointing to a list script or registry.
- A registry contains full implementation instructions instead of concise metadata.
- A shared asset directory is used without owner, provenance, allowed-use, and forbidden-use rules.
- A resolver asks the agent to infer from all implementation bodies instead of structured cues.

## Boundary Validation Signals

A boundary validator should flag or fail when:

- A `SKILL.md` file becomes too large for orchestration.
- A `SKILL.md` file contains many implementation paths or asset paths.
- A growing family has a registry but no list/resolve/materialize scripts.
- A family has implementation directories but no documented normal-use load policy.
- The README duplicates internal implementation catalogs.

## Maintenance Exception

Direct reads are allowed during maintenance. When doing maintenance, keep the scope explicit:

- identify the selected skill and family
- identify the specific implementation or registry being edited
- avoid broad sibling reads unless the task is comparison, migration, or audit
- run the family and repository validators before final delivery
