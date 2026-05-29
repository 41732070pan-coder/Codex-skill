# Overlay / Decorator Contract

Use this contract when a skill has a stable base behavior and users often ask for temporary, local, or preference-driven adjustments that should not become new concrete implementations by default.

## Position

Overlay/decorator support is a repository-level pattern, not a mandatory requirement for every skill. Add it only when a skill has a meaningful base artifact or implementation and user requests commonly modify that base without changing its identity.

Do not require a decorator layer for simple skills with one fixed behavior, pure lookup skills, or tasks where every request is already fully described by ordinary inputs and constraints.

## When To Add An Overlay Layer

Add an overlay/decorator contract when:

- The skill has a base implementation, template, style, provider, mode, strategy, or artifact shape that should remain recognizable.
- Users ask for variations such as tone, palette, motif, layout density, safety strictness, output format details, examples, locale, or temporary assets.
- The requested variation should be accepted, downgraded, or rejected without creating a new implementation entry.
- The skill needs a clear answer to “does the user preference override the base invariant?”
- Quality gates must verify both the base behavior and the requested variation.

Prefer a new implementation family entry instead when:

- The variation becomes a reusable named behavior.
- The variation needs its own assets, registry metadata, prompts, provider, validator, or lifecycle status.
- The base invariants would no longer pass after composition.
- Users need to discover or select the variation by name across future tasks.

## Core Shapes

```ts
type OverlayTarget =
  | "palette"
  | "motif"
  | "texture"
  | "layout"
  | "mood"
  | "tone"
  | "asset"
  | "format"
  | "safety"
  | "example"
  | string;

type OverlayOperation = "add" | "replace" | "increase" | "decrease" | "tint" | "constrain" | "adapt";
type OverlayPriority = "hard" | "soft";
type OverlayIntensity = "subtle" | "balanced" | "expressive";
type OverlaySource = "skill-owned" | "user-provided" | "generated" | "shared-provider" | "code-native" | "none";

interface SkillOverlay {
  id: string;
  target: OverlayTarget;
  operation: OverlayOperation;
  priority: OverlayPriority;
  intensity?: OverlayIntensity;
  source?: OverlaySource;
  value: string | Record<string, unknown>;
  compatibilityRules: string[];
  selfCheckRules?: string[];
}

interface ComposedSkillPlan {
  baseId: string;
  overlays: SkillOverlay[];
  acceptedChanges: string[];
  rejectedOrDowngradedChanges: string[];
  outputPlan?: Record<string, unknown>;
  resourcePlan?: Record<string, unknown>;
  selfCheckPlan: string[];
}

interface OverlayComposer {
  compose(base: unknown, overlays: SkillOverlay[]): ComposedSkillPlan;
}
```

## Required Composition Semantics

1. Resolve the base skill behavior or selected implementation before composing overlays.
2. Extract overlay candidates from explicit user wording, constraints, source assets, examples, and output requirements.
3. Read base invariants from the skill contract, selected implementation, resource policy, and quality gate.
4. Accept compatible overlays, downgrade over-strong overlays, and reject overlays that violate base invariants, asset/source policy, or safety requirements.
5. Record every downgrade or rejection in `rejectedOrDowngradedChanges` when it changes the final output.
6. Run both the base quality gate and overlay-specific self-checks before delivery.

## Design Rules

- Base invariants outrank soft overlays.
- A `replace` operation is risky and must be explicit; replacing identity, safety, provenance, or required structure usually means selecting or creating a new implementation.
- `expressive` overlays should be labeled as variants of the base. If they recur, promote them into an implementation family entry.
- Overlay assets are not base assets unless the skill-owned manifest declares them.
- Overlays should compose with a selected implementation; they should not force the main `SKILL.md` to branch on every variation.
- Keep overlay contracts in references, not in the top-level `SKILL.md`, unless the skill is tiny and the overlay rules are fewer than a few bullets.

## Relationship To Implementation Families

Use an implementation family for durable selectable behaviors. Use overlays for temporary changes to a selected behavior. A mature skill may use both:

```text
Skill workflow
  -> resolve implementation family entry
  -> extract overlays
  -> compose selected implementation + overlays
  -> run base implementation checks + overlay checks
```

For example, a design skill may resolve `seu_design_style` as the base implementation, then apply a temporary maple/deep-crimson overlay. If that overlay becomes a durable named template with its own assets and validator, promote it to a registered implementation.

## Minimal Documentation Checklist

When adding overlay support to a skill, document:

- The normalized request field that stores overlays.
- The overlay data shape or reference file.
- Base invariants overlays must not break.
- Allowed and forbidden overlay sources.
- Conflict handling and downgrade behavior.
- Whether expressive overlays should become variants or new implementations.
- Overlay self-check rules and any runnable validation.
