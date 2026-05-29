# Implementation Family Contract

Use this contract when one skill owns multiple interchangeable concrete implementations. Examples include design styles, render providers, export adapters, analysis strategies, prompt variants, modes, templates, or asset providers.

## Purpose

An implementation family prevents a skill from becoming a large hand-written catalog. It gives agents a deterministic way to discover candidates, resolve or recommend a registered implementation, and load only the selected implementation.

The family contract should be upgrade-compatible: a small family may start as a concise registry table, but it must use the same ids, paths, statuses, aliases/cues, ambiguity semantics, and fallback semantics that later scripted and machine-readable versions will use.

## When A Family Is Required

Create an implementation family when any of these are true:

- The skill has three or more interchangeable implementations and more are expected.
- The implementation list may grow beyond what should be shown in `SKILL.md`.
- Users can request implementations by name, alias, domain cue, medium, provider, or mode.
- Implementations have separate assets, provenance, safety rules, or quality checks.
- Selection and recommendation logic should be deterministic enough to validate in scripts.

## Upgrade-Compatible Family Profiles

Use one family model with increasing maturity, not incompatible small and large designs.

| Profile | Use when | Source of truth | Required interface |
| --- | --- | --- | --- |
| Single behavior | The skill has only one concrete behavior and no selection problem. | `SKILL.md` plus optional references. | No family required. |
| Small family | A small stable set of implementations is easy to scan and has low ambiguity. | Concise, table-shaped Markdown registry. | Stable ids, implementation paths, status, summaries, aliases/cues, ambiguity policy, fallback policy, selected-only loading. Scripts may be deferred with a documented reason. |
| Scripted family | Implementations are growing, users rely on aliases/cues, ambiguity exists, or agents have mis-selected/read siblings. | Markdown, JSON, or YAML registry with the same entry semantics. | List, resolve, get/materialize, and validate commands. |
| Machine-readable family | CI validation, generated catalogs, many entries, status/deprecation rules, asset roots, or high selection risk matter. | JSON/YAML registry plus schema; Markdown is generated or a human-facing mirror. | Schema validation, scripted resolution, scripted materialization, and family-specific validation. |

Upgrade by preserving the registry entry semantics and changing the source-of-truth format or adding scripts. Do not duplicate hand-maintained data across Markdown and machine-readable registries.

## Core Types

```ts
type ImplementationKind = "style" | "provider" | "strategy" | "adapter" | "mode" | "template" | string;
type FamilyLoadPolicy = "registry-only" | "single-implementation-only";
type DirectReadPolicy = "forbidden-during-normal-use" | "maintenance-only";
type FallbackPolicy = "none" | "recommend-registered" | "allow-generic";

interface ImplementationFamily {
  familyName: string;
  ownerSkill: string;
  kind: ImplementationKind;
  registryPath: string;
  registryFormat: "json" | "yaml" | "markdown" | "markdown-generated";
  listCommand?: string;
  resolveCommand?: string;
  materializeCommand?: string;
  validateCommand?: string;
  implementationRoot?: string;
  profile: "small" | "scripted" | "machine-readable";
  defaultLoadPolicy: FamilyLoadPolicy;
  directReadPolicy: DirectReadPolicy;
  scriptDeferralReason?: string;
}

interface ImplementationEntry {
  id: string;
  displayName: string;
  status: "draft" | "experimental" | "stable" | "deprecated";
  summary: string;
  implementationPath: string;
  aliases?: string[];
  exactAliases?: string[];
  contextualAliases?: string[];
  domainCues?: string[];
  mediumCues?: string[];
  negativeCues?: string[];
  ambiguityRisks?: string[];
  assetRoot?: string | "none";
  priority?: "explicit-only" | "domain-default" | "fallback-never";
  fallbackPolicy?: FallbackPolicy;
}

interface ImplementationResolution {
  ok: boolean;
  status: "resolved" | "ambiguous" | "unresolved" | "recommended";
  implementationId?: string;
  confidence?: "explicit" | "strong" | "medium" | "weak";
  reason: string;
  candidates?: Array<{ id: string; summary?: string; reason: string }>;
  recommendation?: { id: string; summary?: string; reason: string };
  nextCommand?: string;
}
```

## Resolution And Recommendation Semantics

Resolution and recommendation must be registry-driven, not hard-coded in `SKILL.md`, resolver source code, or implementation-body browsing. Resolver code should implement generic matching and ranking rules over registry data.

Use this priority order unless the family contract documents a stricter policy:

1. Exact implementation id.
2. Exact alias with no ambiguity.
3. Exact alias plus supporting domain, locale, medium, asset, or task cues.
4. Strong domain/provider/mode cue that maps to one eligible implementation.
5. Contextual or weak cue with insufficient support: return `ambiguous` with candidate ids, summaries, and match reasons for LLM choice.
6. No exact registered candidate: return `unresolved` plus available implementation ids, summaries, and nearest-match reasons when useful, so the LLM can recommend a registered option.

A resolver must not:

- infer by reading implementation bodies;
- hide family-specific alias facts only in code instead of registry data;
- invent, synthesize, or blend an implementation that is not present in the registry;
- select a deprecated implementation implicitly;
- present a recommendation as an exact match.

When resolution is ambiguous or unresolved, use the same fallback pattern: expose the available registered implementations and concise descriptions to the LLM, then let the LLM choose the most likely intended implementation or recommend a close registered implementation. If no useful registered implementation exists, offer a skill-extension path.

## Required Script Interface

Each growing implementation family should expose scripts with these behaviors. Names may vary, but the family contract must document the exact commands. Small families may defer scripts only when the registry is concise, parseable, low-ambiguity, and explicitly documents the deferral reason and upgrade trigger.

| Script role | Required behavior |
| --- | --- |
| List | Return candidate ids, display names, summaries, and match hints without reading implementation bodies. Support filters such as query, medium, kind, status, and limit when useful. |
| Resolve | Accept explicit id/alias and optional query/medium/domain cues. Return one resolved implementation, an ambiguous candidate list, or an unresolved result with available implementation summaries for LLM choice/recommendation. |
| Materialize / get | Return only the selected implementation content needed for the current task. Support section, medium, mode, or output filtering where implementation files can be large. |
| Validate | Check registry shape, unique ids and aliases, ambiguous cues, existing implementation paths, asset roots, required sections, fallback policies, and family-specific contracts. |

## Loading Rules

- `SKILL.md` explains the family workflow and dispatch interface; it does not list every implementation once the family can grow.
- The registry is the discovery surface. It contains concise metadata, not full implementation instructions.
- During normal use, agents use the registry or run list/resolve before loading implementation content; ambiguous or unresolved results should include candidate metadata for LLM choice/recommendation.
- Agents load implementation content through the selected `implementationPath` or materialize/get script and only for the selected implementation.
- Direct implementation-file reads are allowed for maintenance, debugging, validation authoring, or editing a scoped implementation.
- Assets follow the selected implementation's declared asset policy and manifest; do not browse sibling implementation assets for decoration.

## Registry Requirements

A family registry must include enough metadata to support deterministic discovery and future scripting:

| Field | Requirement |
| --- | --- |
| `id` | Stable machine id, unique within the family. |
| `displayName` | Human-readable label. |
| `status` | Lifecycle state. Deprecated entries are never selected implicitly. |
| `summary` | Short option text safe to show when asking the user to choose. |
| `implementationPath` | Path to the concrete implementation, loaded only after resolution or during maintenance. |
| `aliases` / `exactAliases` | Names users may type that are safe for direct matching. Aliases should be unique or explicitly disambiguated. |
| `contextualAliases` / `domainCues` | Weak or contextual cues that require supporting context or clarification. |
| `negativeCues` | Terms that should prevent a misleading match. |
| `ambiguityRisks` | Known overlap risks and when to ask instead of choosing. |
| `fallbackPolicy` | Missing or weak-match behavior; default to `recommend-registered` when safe, and label recommendations instead of silently substituting. |
| `assetRoot` | Asset directory or `none`; asset roots require manifests. |

## Upgrade Triggers

Upgrade a small family to scripted or machine-readable form when any of these become true:

- More than five implementations exist or are expected soon.
- The registry table no longer fits a short human scan.
- Aliases or cues overlap across implementations.
- Contextual aliases require locale, domain, or medium-sensitive handling.
- Draft, experimental, deprecated, or explicit-only status rules matter.
- Implementations own assets or external provider configuration.
- Wrong selection has high cost or must be tested in CI.
- An agent has selected the wrong implementation, silently fallen back, or read sibling implementations during normal use.

## `SKILL.md` Boundary

`SKILL.md` may include:

- The family name and purpose.
- The registry location and, when present, list/resolve/materialize command shapes.
- The policy for ambiguous or missing implementation requests.
- A tiny example using one or two placeholder ids.

`SKILL.md` should not include:

- A complete implementation catalog for a growing family.
- Full palettes, prompts, provider internals, adapter code, asset lists, or implementation-specific manuals.
- Instructions to inspect every file under `references/`, `implementations/`, or `assets/` during normal use.
- Hard-coded natural-language aliases that are not represented in the registry.

## Quality Checklist

Before finalizing a family change:

- Registry entries are unique and schema-valid or table-valid for the chosen profile.
- Small-family script deferral is documented with upgrade triggers.
- Exact aliases are unique or explicitly disambiguated.
- Contextual aliases and ambiguity risks lead to `ambiguous`, not forced selection.
- Missing or ambiguous implementations expose available options and summaries for LLM choice/recommendation, or a skill-extension path when no useful option exists.
- List/resolve/materialize scripts work without third-party dependencies unless the dependency is documented.
- Ambiguous resolution returns candidates with summaries instead of blending implementations.
- Materialization returns one selected implementation, not the whole family.
- Asset roots and manifests are scoped to the selected implementation.
- `SKILL.md` points to registry/scripts and policies rather than fan-out lists.
- Boundary validation and family-specific validators pass, or manual validation is documented for a small family.
