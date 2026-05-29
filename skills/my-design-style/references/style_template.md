# <style_name>

Use `<style_name>` for <primary use cases>. It should feel <personality words>.

## Contract Conformance

Implements `DesignStyleBase` as `<ImplementationClass>`.

Required runtime sections: Triggers, Intent, Anti-Goals, Color Tokens, Typography, Layout Principles, PPT Slide Archetypes, Visual Rhythm System, Web Translation, App / Dashboard Translation, Static Visual Translation, Asset Interface, Surface Texture Policy, Asset Rules, Modifier Compatibility, Preview Option Sets, Self-Check.

## Triggers

Use this style when the user asks for:

- Exact names and aliases.
- Domain cues.
- Medium cues.
- Default and non-default selection rules.

## Intent

Define the design purpose, impression, and reusable behavior.

## Anti-Goals

- List visual clichés to avoid.
- List legal, brand, or accessibility hazards.
- List outcomes that would make the style generic or off-style.

## Color Tokens

| Token | Hex | Role |
| --- | --- | --- |
| `<style>-primary` | `#000000` | Primary identity or hierarchy role. |

### Series Color Cards

| Series | Primary | Auxiliary Colors | Neutral / Base | Use |
| --- | --- | --- | --- | --- |
| Default | `#000000` | `#666666`, `#999999` | `#FFFFFF`, `#111111` | Default use. |

### Same-Family Progression Cards

| Family | Primary | Support-Strong | Support-Mid | Support-Soft | Wash | Muted-Bridge |
| --- | --- | --- | --- | --- | --- | --- |
| Default | `#000000` | `#333333` | `#666666` | `#999999` | `#EEEEEE` | `#777777` |

## Palette Recipes

| Recipe | Palette | Use |
| --- | --- | --- |
| Default | `<tokens>` | <use case> |

## Typography

- Primary font attitude.
- Heading/body/caption hierarchy.
- Numeral behavior.
- Fallbacks.

## Layout Principles

- Grid.
- Spacing scale.
- Density.
- Hierarchy.
- Composition rules.

## PPT Slide Archetypes

| Archetype | Purpose | Style notes |
| --- | --- | --- |
| Cover | Title and context | <rules> |

## Visual Rhythm System

For multi-page or multi-screen artifacts, define a deck/page-level variation plan before generating details. The plan must keep the style recognizable while preventing monotonous repeated layouts.

- `rhythmScope`: single surface | multi-slide deck | multi-screen flow | long page.
- `visualAnchorRule`: every slide/screen/major section needs at least one non-body-text visual anchor such as a diagram, chart, swatch, label frame, rail, callout, motif, image, or texture treatment.
- `archetypeVarietyRule`: do not use the same layout skeleton too many times in sequence; vary scale, columns, anchor placement, and density by information role.
- `motifRotation`: rotate approved style motifs or explicitly use `motif-off` when content density requires it.
- `assetFallbackRule`: compare runtime assets, approved network-sourced candidates, code-native geometry, typography, color blocks, diagrams, and user-provided assets; choose the style-faithful option that best prevents empty or monotonous surfaces.
- `antiMonotonyCheck`: verify that visual anchors, archetypes, motif treatments, and density levels vary across the artifact without becoming decorative clutter.

## Web Translation

Define page structure, tokens, responsive behavior, and component states.

## App / Dashboard Translation

Define navigation, tables, charts, filters, state colors, and responsive constraints.

## Static Visual Translation

Define poster/image/card/social/diagram behavior, aspect ratios, safe text zones, and motif density.

## Asset Interface

- `assetRoot`: `assets/<style_name>/` or `none`.
- `importMode`: `style-owned`, `none`, or `user-provided-only`.
- `manifestFile`: optional opaque provenance handle; do not require the framework to inspect it.
- `availableAssets`: abstract handles or roles; do not enumerate file names or assert folder contents.
- `usageRoles`: approved roles.
- `placementRules`: aspect ratio, contain/crop/repeat behavior, opacity, and safe regions.
- `fallbackPolicy`: what to do when runtime assets are unavailable, unapproved, or inappropriate.

## Surface Texture Policy

Declare whether this style may use a surface provider. Provider contents under `assets/` are opaque; the template records stable handles, tokens, and fallback behavior without describing current files.

- `provider`: `none` by default; otherwise a stable provider handle allowed by the style family.
- `assetRoot`: `none` by default; otherwise an opaque `assets/<provider_name>/` boundary.
- `manifestFile`: `none` when disabled; otherwise an opaque provider manifest handle.
- `indexFile`: `none` when disabled; otherwise an opaque provider index handle.
- `provenanceFile`: `none` when disabled; otherwise an opaque provider provenance handle.
- `defaultToken`: `none` when disabled; otherwise one declared texture token.
- `allowedTokens`: texture tokens allowed for this style; use `[]` when disabled.
- `opacityRange`: low-opacity bounds for background and panel usage; use `[0, 0]` when disabled.
- `allowedSurfaces`: where texture may appear; use `[]` when disabled.
- `forbiddenSurfaces`: where texture must not appear; use `[]` when disabled.
- `fallbackPolicy`: what to do when texture is unavailable or harms contrast.

## Asset Rules

- Preserve intrinsic aspect ratio.
- Use only the active style's assets.
- Avoid generic downloaded filler.
- Explain legal or brand constraints.

## Modifier Compatibility

Every concrete style must implement `DesignStyleBase.getModifierCompatibility()` here. State whether modifiers are accepted and how the abstract workflow should accept, downgrade, or reject them. Use restrictive values if this style should not accept modifiers beyond ordinary constraints.

- `acceptsModifiers`: true | false.
- `allowedTargets`: palette, motif, texture, layout, mood, asset, or none.
- `allowedSources`: style-owned, user-provided, generated-vector, shared-provider, code-native, none.
- `defaultIntensity`: subtle | balanced | expressive.
- `conflictPolicy`: <base invariants that outrank modifiers and downgrade/reject rules>.
- `promotionPolicy`: <when a recurring expressive modifier becomes a new concrete style>.

Hard invariants:

- <Rules modifiers must not break.>

Allowed soft modifiers:

- <Modifier types this style can accept.>

Modifier self-check additions:

- <Checks to run in addition to the base style self-check.>

## Preview Option Sets

`getPreviewOptions(request, composedPlan)` exposes preview choices. In `previewMode: auto`, explicit preview is used only when ambiguity, stakes, brand or cultural sensitivity, or user request requires it. Otherwise the model creates an internal `StyleLock` from the default option sets and proceeds. Apply approved or internally locked choices through `applyStyleLock(styleLock, composedPlan)` so the final output matches the locked preview decisions.

- `previewSurface`: combined style board plus small artifact sample.
- `defaultOptionSets`: palette, texture when enabled, layout density, mood, asset or motif when relevant.
- `styleLockRules`: record selected options, rejected or downgraded changes, and locked decisions; do not silently change them during final generation.

| Option Set | Target | Default | Options | Rules |
| --- | --- | --- | --- | --- |
| `<option-set-id>` | palette / texture / layout / mood / asset | `<default-option-id>` | `<option ids>` | Must preserve style invariants and accessibility. |

## Self-Check

Return or simulate this `CheckResult` shape before finishing:

- `ok`: true only when no required fixes remain.
- `issues`: concrete style, readability, layout, asset, or medium-specific problems.
- `requiredFixes`: required revisions before delivery.

Minimum checks:

- Style fidelity.
- Contrast and readability.
- Alignment and spacing.
- Visual anchor coverage, archetype variety, motif rotation, and anti-monotony behavior for multi-surface outputs.
- Overflow/responsiveness.
- Asset legality, role fit, and non-distortion.
- Medium-specific correctness.
