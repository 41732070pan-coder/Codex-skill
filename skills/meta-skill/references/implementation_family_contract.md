# Implementation Family Contract

Use this contract when one skill owns multiple interchangeable concrete implementations. Examples include design styles, render providers, export adapters, analysis strategies, prompt variants, modes, templates, or asset providers.

## Purpose

An implementation family prevents a skill from becoming a large hand-written catalog. It gives agents a deterministic way to discover candidates, resolve the requested implementation, and load only the selected implementation.

## When A Family Is Required

Create an implementation family when any of these are true:

- The skill has three or more interchangeable implementations and more are expected.
- The implementation list may grow beyond what should be shown in `SKILL.md`.
- Users can request implementations by name, alias, domain cue, medium, provider, or mode.
- Implementations have separate assets, provenance, safety rules, or quality checks.
- Selection logic should be deterministic enough to validate in scripts.

## Core Types

```ts
type ImplementationKind = "style" | "provider" | "strategy" | "adapter" | "mode" | "template" | string;
type FamilyLoadPolicy = "registry-only" | "single-implementation-only";
type DirectReadPolicy = "forbidden-during-normal-use" | "maintenance-only";

interface ImplementationFamily {
  familyName: string;
  ownerSkill: string;
  kind: ImplementationKind;
  registryPath: string;
  registryFormat: "json" | "yaml" | "markdown" | "markdown-generated";
  listCommand: string;
  resolveCommand: string;
  materializeCommand: string;
  validateCommand: string;
  implementationRoot?: string;
  defaultLoadPolicy: FamilyLoadPolicy;
  directReadPolicy: DirectReadPolicy;
}

interface ImplementationEntry {
  id: string;
  displayName: string;
  status: "draft" | "experimental" | "stable" | "deprecated";
  aliases: string[];
  domainCues: string[];
  mediumCues?: string[];
  summary: string;
  implementationPath: string;
  assetRoot?: string | "none";
  priority?: "explicit-only" | "domain-default" | "fallback-never";
}

interface ImplementationResolution {
  ok: boolean;
  status: "resolved" | "ambiguous" | "unresolved";
  implementationId?: string;
  confidence?: "explicit" | "strong" | "medium" | "weak";
  reason: string;
  candidates?: Array<{ id: string; reason: string }>;
  nextCommand?: string;
}
```

## Required Script Interface

Each growing implementation family should expose scripts with these behaviors. Names may vary, but the family contract must document the exact commands.

| Script role | Required behavior |
| --- | --- |
| List | Return candidate ids, display names, summaries, and match hints without reading implementation bodies. Support filters such as query, medium, kind, status, and limit when useful. |
| Resolve | Accept explicit id/alias and optional query/medium/domain cues. Return one resolved implementation, an ambiguous candidate list, or an unresolved result. |
| Materialize / get | Return only the selected implementation content needed for the current task. Support section, medium, mode, or output filtering where implementation files can be large. |
| Validate | Check registry shape, unique ids and aliases, existing implementation paths, asset roots, required sections, and family-specific contracts. |

## Loading Rules

- `SKILL.md` explains the family workflow and script interface; it does not list every implementation once the family can grow.
- The registry is the discovery surface. It contains concise metadata, not full implementation instructions.
- During normal use, agents run list/resolve before loading implementation content.
- Agents load implementation content through the materialize/get script and only for the selected implementation.
- Direct implementation-file reads are allowed for maintenance, debugging, validation authoring, or editing a scoped implementation.
- Assets follow the selected implementation's declared asset policy and manifest; do not browse sibling implementation assets for decoration.

## Registry Requirements

A family registry must include enough metadata to support deterministic discovery:

| Field | Requirement |
| --- | --- |
| `id` | Stable machine id, unique within the family. |
| `displayName` | Human-readable label. |
| `status` | Lifecycle state. Deprecated entries are never selected implicitly. |
| `aliases` | Names users may type. Aliases should be unique or explicitly disambiguated. |
| `domainCues` | Task/domain cues that can support implicit resolution. |
| `summary` | Short option text safe to show when asking the user to choose. |
| `implementationPath` | Path to the concrete implementation, loaded only after resolution or during maintenance. |
| `assetRoot` | Asset directory or `none`; asset roots require manifests. |

## `SKILL.md` Boundary

`SKILL.md` may include:

- The family name and purpose.
- The list/resolve/materialize command shapes.
- The policy for ambiguous or missing implementation requests.
- A tiny example using one or two placeholder ids.

`SKILL.md` should not include:

- A complete implementation catalog for a growing family.
- Full palettes, prompts, provider internals, adapter code, asset lists, or implementation-specific manuals.
- Instructions to inspect every file under `references/`, `implementations/`, or `assets/` during normal use.

## Quality Checklist

Before finalizing a family change:

- Registry entries are unique and schema-valid.
- List/resolve/materialize scripts work without third-party dependencies unless the dependency is documented.
- Ambiguous resolution returns candidates instead of blending implementations.
- Materialization returns one selected implementation, not the whole family.
- Asset roots and manifests are scoped to the selected implementation.
- `SKILL.md` points to scripts and policies rather than fan-out lists.
- Boundary validation and family-specific validation are recorded in the final response.
