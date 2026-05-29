# Style Registry

This registry is the concrete-class registry for `my-design-style`. Load only the reference file for the style needed by the user.

In framework terms:

- `SKILL.md` defines the abstract class `DesignStyleBase` and required interfaces.
- This file maps style names to concrete implementations.
- Each `references/<style_name>.md` file implements the same design contract.

| Style | Reference | Concrete class role | Use when |
| --- | --- | --- | --- |
| `seu_design_style` | `seu_design_style.md` | Institutional academic style implementation | Academic, institutional, Southeast University, thesis defense, research report, campus-branded PPT, web, or app design. |
| `renminbi_color_style` | `renminbi_color_style.md` | Banknote-inspired financial-cultural style implementation | RMB, yuan, Chinese banknote, finance, commerce, fintech, auction, collection, and culturally Chinese value-oriented PPT, web, app, or dashboard design. |
| `chinese_traditional_color_style` | `chinese_traditional_color_style.md` | Traditional Chinese color-system style implementation | Chinese traditional colors, guofeng, classical Chinese, cultural, museum, editorial, brand, PPT, web, app, or dashboard design using named traditional palettes. |


## Registry Entry Shape

Treat each row as a lightweight class-registration record. When a style list grows, keep this metadata explicit instead of adding custom branches in `SKILL.md`.

```ts
interface StyleRegistryEntry {
  styleName: string;
  referenceFile: `references/${string}.md`;
  aliases: string[];
  domainCues: string[];
  mediumCues: TargetMedium[];
  priority: "explicit-only" | "domain-default" | "fallback-never";
  assetRoot: `assets/${string}/` | "none";
}
```

## Resolution Rules

Resolve styles like a registry lookup plus a confidence score:

- Exact style name or alias wins.
- Strong domain cue plus matching medium wins when no explicit style is named.
- If two concrete styles match with similar confidence, ask once instead of blending them.
- Do not mix concrete style files unless the user explicitly requests a hybrid; a hybrid should still name one primary style and one secondary influence.
- Never use assets from a style that is not the active concrete implementation.

## Adding A New Style

Create `references/<style_name>.md` and add one row to this registry.

A new style must behave like a concrete implementation of `DesignStyleBase`: it can make different visual decisions, but it must expose the same categories of information so the main workflow can use it without custom branching.

Each style file should implement:

- `TriggerMatcher`: names, aliases, domain cues, and selection rules.
- `DesignIntentProvider`: design intent, intended use cases, and anti-goals.
- `PaletteProvider`: semantic color tokens and same-family progression cards following `design_mechanics.md`.
- `TypographyProvider`: font attitude, hierarchy, weight, spacing, and fallbacks.
- `LayoutSystem`: grid, spacing, density, rhythm, and composition rules.
- `ComponentTranslator`: PPT slide archetypes plus web, app, dashboard, and static visual translation rules.
- `AssetPolicy`: permitted style-owned assets, placement rules, fallback behavior, and distortion constraints.
- `SurfaceTexturePolicy`: optional shared substrate textures, allowed texture tokens, opacity ranges, allowed surfaces, and raster-first format policy.
- `QualityGate`: self-check criteria for contrast, alignment, overflow, responsiveness, and style fidelity.

Keep style files independent. Shared logic belongs in `SKILL.md` or `design_mechanics.md`; style-specific decisions belong in the style file.

## Implementation Map Requirement

Every concrete style file should contain an `Implementation Map` table near the top. It is the equivalent of a class/interface conformance checklist and should map each required interface to the sections that implement it.

Use this shape:

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

If a style has no bundled assets, its `AssetPolicy` must still explicitly say `assetRoot: none` and define the fallback behavior. If it does have assets, it should expose a manifest such as `assets/<style_name>/ASSET_MANIFEST.md`.
