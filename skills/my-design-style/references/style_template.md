# <style_name>

Use `<style_name>` for <primary use cases>. It should feel <personality words>.

## Implementation Map

| Interface | Implemented by |
| --- | --- |
| `TriggerMatcher` | `Triggers` |
| `DesignIntentProvider` | `Intent`, `Anti-Goals` |
| `PaletteProvider` | `Color Tokens`, `Series Color Cards`, `Same-Family Progression Cards`, `Palette Recipes` |
| `TypographyProvider` | `Typography` |
| `LayoutSystem` | `Layout Principles` |
| `ComponentTranslator` | `PPT Slide Archetypes`, `Web Translation`, `App / Dashboard Translation`, `Static Visual Translation` |
| `AssetPolicy` | `Asset Interface`, `Asset Rules` |
| `SurfaceTexturePolicy` | `Surface Texture Policy` |
| `QualityGate` | `Self-Check` |

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

## Web Translation

Define page structure, tokens, responsive behavior, and component states.

## App / Dashboard Translation

Define navigation, tables, charts, filters, state colors, and responsive constraints.

## Static Visual Translation

Define poster/image/card/social/diagram behavior, aspect ratios, safe text zones, and motif density.

## Asset Interface

- `assetRoot`: `assets/<style_name>/` or `none`.
- `importMode`: `style-owned`, `none`, or `user-provided-only`.
- `manifestFile`: optional path to `ASSET_MANIFEST.md` or equivalent.
- `availableAssets`: approved files or `none`.
- `usageRoles`: approved roles.
- `placementRules`: aspect ratio, contain/crop/repeat behavior, opacity, and safe regions.
- `fallbackPolicy`: what to do when no style-owned asset is available.

## Surface Texture Policy

Declare whether this style may use a bundled surface provider. The canonical provider source is Transparent Textures (`https://www.transparenttextures.com/`), but default to disabled unless all selected provider files, manifest rows, index entries, and provenance notes exist.

- `provider`: `none` by default; use `transparent_textures` only after adding the sourced files, provider manifest, index, and provenance.
- `assetRoot`: `none` by default; otherwise a real `assets/<provider_name>/` path.
- `manifestFile`: optional, and only when the file exists.
- `defaultToken`: one approved texture token, or omit when disabled.
- `allowedTokens`: texture tokens allowed for this style; use an empty list when disabled.
- `opacityRange`: low-opacity bounds for background and panel usage; use `[0, 0]` when disabled.
- `allowedSurfaces`: where texture may appear; use an empty list when disabled.
- `forbiddenSurfaces`: where texture must not appear.
- `fallbackPolicy`: what to do when texture is unavailable or harms contrast.

## Asset Rules

- Preserve intrinsic aspect ratio.
- Use only the active style's assets.
- Avoid generic downloaded filler.
- Explain legal or brand constraints.

## Self-Check

Return or simulate this `CheckResult` shape before finishing:

- `ok`: true only when no required fixes remain.
- `issues`: concrete style, readability, layout, asset, or medium-specific problems.
- `requiredFixes`: required revisions before delivery.

Minimum checks:

- Style fidelity.
- Contrast and readability.
- Alignment and spacing.
- Overflow/responsiveness.
- Asset legality, role fit, and non-distortion.
- Medium-specific correctness.
