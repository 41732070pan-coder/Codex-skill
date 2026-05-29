---
name: my-design-style
description: Extensible visual design system for PPT decks, websites, apps, dashboards, and frontend demos. Use when Codex needs to design or restyle presentation slides, web pages, app screens, UI components, templates, or design assets in a named house style such as seu_design_style, renminbi_color_style, or chinese_traditional_color_style, and when future styles need to be added under the same my_design_style framework.
---

# My Design Style

## Purpose

Use this skill to turn a requested artifact into a polished visual design using one named style from the `my_design_style` family.

## Triggers And Non-Triggers

| Type | Cues |
| --- | --- |
| Trigger | Design or restyle PPT decks, webpages, app screens, dashboards, UI components, templates, or static visual assets. |
| Trigger | Apply a named house style such as `seu_design_style`, `renminbi_color_style`, or `chinese_traditional_color_style`. |
| Trigger | Add or validate a new concrete style inside the `my-design-style` framework. |
| Non-trigger | Repository-level skill governance, renaming, registry policy, or quality-gate design belongs to `meta-skill`. |
| Ask if ambiguous | The user wants a generic image or illustration rather than a reusable design-system translation. |

## Inputs And Outputs

| Contract | Details |
| --- | --- |
| Required inputs | Target artifact or design task, intended medium, content goal, and selected style or enough cues to resolve one. |
| Optional inputs | Brand constraints, dimensions, source assets, accessibility requirements, output format, and platform constraints. |
| Normalized shape | `DesignRequest` with medium, goal, audience/context, hard constraints, selected style, asset policy, and output requirements. |
| Outputs | Style-guided design specifications, PPT/UI/web/dashboard guidance, generated visual assets, or implementation-ready code guidance. |
| Failure modes | Ask before proceeding when no concrete style can be resolved or when requested assets lack provenance or safe usage rules. |

## References

Load only the references needed for the selected style or extension task. Use `references/style_registry.md` to resolve available styles, `references/style_contract.md` when validating interfaces, `references/style_template.md` when adding a style, `references/design_mechanics.md` for shared mechanics, and one concrete `references/<style_name>.md` for the active style.

Treat `my-design-style` as a small design framework:

- `SKILL.md` is the abstract base class and orchestration layer.
- `references/style_contract.md` defines the formal interfaces and typed data contracts.
- `references/design_mechanics.md` provides shared utilities and reusable mechanics.
- `references/style_registry.md` is the concrete-style registry.
- `references/<style_name>.md` files are concrete implementations.
- `assets/` contains style-owned resources and explicitly registered shared substrate providers. Identity/ornament assets remain style-owned; neutral surface textures live in `assets/transparent_textures/` and require style opt-in.

Current concrete styles include `seu_design_style`, `renminbi_color_style`, and `chinese_traditional_color_style`.

## Programming Model

### Abstract Class: `DesignStyleBase`

For the full data contract, optional interfaces, and asset-provider shape, read `references/style_contract.md`.

All styles conceptually extend this abstract class. Do not put style-specific decisions in `SKILL.md`; put only shared control flow, contracts, and invariant rules here.

```ts
abstract class DesignStyleBase implements
  TriggerMatcher,
  DesignIntentProvider,
  PaletteProvider,
  TypographyProvider,
  LayoutSystem,
  ComponentTranslator,
  AssetPolicy,
  SurfaceTexturePolicy,
  QualityGate {
  abstract name: string;
  abstract referenceFile: string;
  abstract match(request: DesignRequest): boolean;
  abstract getDesignIntent(): DesignIntent;
  abstract getAntiGoals(): AntiGoal[];
  abstract getColorSystem(): ColorSystem;
  abstract getTypographySystem(): TypographySystem;
  abstract getLayoutRules(): LayoutRules;
  abstract translateToMedium(medium: TargetMedium): MediumRules;
  abstract getAssetRules(): AssetRules;
  abstract getSurfaceTexturePolicy(): SurfaceTexturePolicy;
  abstract selfCheck(output: Artifact): CheckResult;
}
```

Use this abstraction to keep every style substitutable: once a style is selected, the workflow should not need custom branches except for loading its reference file.

### Template Method

The base skill owns the workflow. Concrete style files own only the answers to the interface methods.

```ts
function renderWithDesignStyle(request: DesignRequest): Artifact {
  const normalizedRequest = buildDesignRequest(request);
  const style = resolveStyle(normalizedRequest);
  const intent = style.getDesignIntent();
  const palette = style.getColorSystem();
  const typography = style.getTypographySystem();
  const layout = style.getLayoutRules();
  const assets = style.getAssetRules();
  const texturePolicy = style.getSurfaceTexturePolicy();
  const mediumRules = style.translateToMedium(normalizedRequest.medium);
  const artifact = composeArtifact({
    request: normalizedRequest,
    style,
    intent,
    palette,
    typography,
    layout,
    assets,
    texturePolicy,
    mediumRules,
  });

  return style.selfCheck(artifact).ok ? artifact : reviseArtifact(artifact);
}
```

This is the invariant path for every style. If a future style seems to need a special branch, first ask whether that behavior belongs in a new interface method, a shared mechanic, or a medium translator.

### Interfaces

Each concrete style reference must satisfy these interfaces:

- `TriggerMatcher`: declares names, aliases, domain cues, and when the style should be selected.
- `DesignIntentProvider`: defines desired impression, use cases, and explicit anti-goals.
- `PaletteProvider`: provides role-based color tokens and same-family progression cards.
- `TypographyProvider`: defines font attitude, hierarchy, weight, spacing, and fallback behavior.
- `LayoutSystem`: defines spacing, grid, density, hierarchy, rhythm, and composition rules.
- `ComponentTranslator`: maps the style into PPT, web, app, dashboard, and static visual patterns.
- `AssetPolicy`: defines style-owned asset folders, allowed identity assets, placement, sizing, and distortion constraints.
- `AssetProvider` when `assetRoot` is not `none`: exposes a style-owned asset module, preferably with an asset manifest, instead of letting the workflow browse `assets/` directly.
- `SurfaceTexturePolicy`: declares whether the style may use shared transparent textures, which tokens are allowed, opacity bounds, and allowed surfaces.
- `QualityGate`: defines visual checks for contrast, alignment, overflow, responsiveness, and style fidelity.

A new style is valid only when it implements all required interfaces in its reference file.

Each concrete reference should include an `Implementation Map` near the top:

| Interface | Required evidence in the style file |
| --- | --- |
| `TriggerMatcher` | Names, aliases, domain cues, and default/non-default selection rules. |
| `DesignIntentProvider` | Intent, use cases, anti-goals, and style personality. |
| `PaletteProvider` | Semantic tokens, source palettes, series cards, and same-family progression cards. |
| `TypographyProvider` | Font attitude, hierarchy, weights, spacing, numeral behavior, and fallbacks. |
| `LayoutSystem` | Grid, spacing, density, composition, rhythm, and content-safe layout rules. |
| `ComponentTranslator` | PPT, web, app, dashboard, and static visual translation rules. |
| `AssetPolicy` | `assetRoot`, approved files or `none`, import mode, manifest path, roles, placement rules, distortion rules, and fallback policy. |
| `SurfaceTexturePolicy` | `provider`, allowed texture tokens, opacity range, target surfaces, forbidden surfaces, and fallback policy. |
| `QualityGate` | A self-check that can reject generic, unreadable, distorted, or off-style output. |

### Concrete Implementations

- `seu_design_style` implements `DesignStyleBase` for academic, institutional, Southeast University, thesis defense, research report, campus-branded PPT, web, or app design. Load `references/seu_design_style.md`.
- `renminbi_color_style` implements `DesignStyleBase` for RMB, yuan, Chinese banknote, finance, commerce, fintech, auction, collection, and culturally Chinese value-oriented designs. Load `references/renminbi_color_style.md`.
- `chinese_traditional_color_style` implements `DesignStyleBase` for Chinese traditional colors, guofeng, classical Chinese, cultural, museum, editorial, brand, PPT, web, app, or dashboard design. Load `references/chinese_traditional_color_style.md`.

## Dispatch Workflow

1. Build a `DesignRequest`:
   - Target medium: PPT/slides, web page, app screen, dashboard, document visual, static image, or design template.
   - Content goal: explain, persuade, compare, report, present, brand, sell, or teach.
   - Audience and context: academic, institutional, financial, cultural, product, executive, public, or internal.
   - Hard constraints: dimensions, platform, accessibility, source assets, brand requirements, output format.
2. Resolve the concrete style:
   - If the user names a known style or alias, load the matching reference file.
   - If the user asks for available styles or future expansion, read `references/style_registry.md`.
   - If no style is named and visual identity materially affects the outcome, ask once.
   - Otherwise default to `seu_design_style` only for SEU, academic defense, campus, or research-report contexts.
3. Instantiate the style by reading only its reference file plus shared resources needed for the task. Read `references/style_contract.md` when adding or validating a style implementation.
4. Apply shared mechanics before medium-specific rendering:
   - Read `references/design_mechanics.md` when the task needs palette construction, same-family gradients, style-owned asset interfaces, shared surface textures, or a new style reference.
   - Build a same-family color progression: `primary`, `support-strong`, `support-mid`, `support-soft`, `wash`, and `muted-bridge`.
   - Resolve assets through the selected concrete style's `AssetPolicy`; never assume a shared ornament library or browse `assets/` without the style exposing that module.
   - Resolve bottom-surface textures through the selected style's `SurfaceTexturePolicy` and `assets/transparent_textures/TEXTURE_MANIFEST.md`; shared textures are optional substrate layers, not motifs.
5. Translate through the selected style interface:
   - For PPT/slides, use slide archetypes, hierarchy, and layout rules from the concrete style.
   - For web/app UI, convert style rules into design tokens, layout rhythm, component states, and responsive behavior.
   - For dashboards, preserve semantic color roles and avoid using decorative color where data meaning is required.
   - For generated images or static visuals, preserve palette, typography attitude, ornament density, and asset placement rules.
6. Apply asset and texture constraints:
   - Use bundled assets only when they serve identity or structure.
   - Avoid scattering logos or decorative motifs as filler.
   - Preserve image and SVG aspect ratios.
   - Before placing identity assets, read intrinsic size from `viewBox`, `width`/`height`, or image metadata.
   - Fit identity assets with contain-style sizing and center alignment unless the concrete style explicitly allows cropping.
   - Never stretch logos, wordmarks, motto artwork, building silhouettes, or cultural motifs to fill arbitrary boxes.
   - Apply shared textures only below content, normally at 2-10% perceived opacity, and remove them if they reduce text or chart legibility.
7. Run the style `QualityGate`:
   - Check alignment, spacing, hierarchy, text overflow, contrast, responsive behavior, image distortion, and decorative relevance.
   - Verify the output still reads as the selected concrete style, not as a generic template with swapped colors.

## Shared Design Mechanics

Shared mechanics belong here or in `references/design_mechanics.md`, not inside one named style. A concrete style may prefer certain mechanics, but the underlying mechanics are framework-level utilities.

### Same-Family Color Progression

Every color-led style must treat a selected color family as a progression, not as a single isolated primary. A practical card should include:

- `primary`: defining hue for titles, section identity, primary actions, or the main data series.
- `support-strong`: neighboring deep or saturated color for non-primary emphasis.
- `support-mid`: middle value for secondary panels, chart companions, selected rows, or comparison marks.
- `support-soft`: softer color for low-pressure emphasis and callouts.
- `wash`: pale version for backgrounds and transition panels.
- `muted-bridge`: grayer or warmer bridge color for neutralized transitions and quiet metadata.

Reserve `primary` for the highest-order message. Use support colors for gradation, partial emphasis, hover/active states, section rhythm, charts, and editorial depth.

### Style-Owned Asset Interface

Assets are concrete-style resources, not a shared decorative library. A style may expose an asset interface only when it has a curated folder and clear usage rules.

Each concrete style decides:

- `assetRoot`: the style-owned folder, such as `assets/seu_design_style/`.
- `importMode`: `style-owned`, `none`, or `user-provided-only`.
- `manifestFile`: optional manifest such as `assets/seu_design_style/ASSET_MANIFEST.md`.
- `availableAssets`: named files or groups that are approved for that style.
- `usageRoles`: how each asset may be used, such as identity mark, wordmark, motto, building silhouette, footer band, side rail, cover anchor, or low-opacity background motif.
- `placementRules`: aspect ratio, contain/crop behavior, opacity, repetition, and safe regions.
- `fallbackPolicy`: what to do when no style-owned asset exists. Prefer clean layout, rules, typography, and generated code-native geometry over downloading arbitrary decorative assets.

Do not create or reference a global shared ornament or identity asset folder. If a future style needs identity assets, add them under `assets/<style_name>/` and document them in that style reference.

### Shared Surface Texture Provider

A limited exception exists for neutral substrate textures. `assets/transparent_textures/` is a shared `SurfaceTextureProvider`, not an ornament library. It may be used only when the active concrete style opts in through `SurfaceTexturePolicy` and the selected texture remains below content as a low-opacity ground layer.

Transparent Textures is modeled as a raster-first provider. The canonical assets are native transparent PNG tiles downloaded from the upstream source. SVG files under `assets/transparent_textures/svg_wrappers/` are adapter wrappers only; they reference PNG tiles and must not be treated as true vector reconstructions.

- Read `references/texture_provider.md` before applying shared textures.
- Read `assets/transparent_textures/TEXTURE_MANIFEST.md` and `assets/transparent_textures/texture_index.json` to resolve token names, file paths, source URLs, tile sizes, recommended opacity, and safe placement.
- For PPT/PDF, precompose the native PNG texture into a full-slide or panel raster at the target size; do not stretch an individual tile.
- For web/app, use repeated PNG background image layers and separate opacity control.
- For SVG-oriented pipelines, use `svg_wrappers/*.pattern.svg` only as an interoperability adapter.
- If contrast or content density suffers, disable the texture and keep the style through color, typography, and layout.

## Extensibility Contract

To add a concrete style implementation:

1. Create `references/<style_name>.md`.
2. Register it in `references/style_registry.md`.
3. Implement every interface listed in `Programming Model`.
4. Keep the file independent: it may reference shared mechanics, but it should not require another concrete style.
5. Add assets only when they are reusable, legally usable, and necessary for identity or structure.

Every style reference should define:

- `name`, aliases, triggers, and intended use cases.
- Design intent and anti-goals.
- Color tokens with semantic roles.
- Series color cards and same-family progression cards.
- Typography guidance.
- Layout, spacing, density, and composition rules.
- Component, dashboard, or slide archetypes.
- Asset usage rules, including style-owned asset folder, approved files, roles, placement, and fallback policy.
- Medium-specific translation for PPT, web, app, dashboard, and static visuals.
- A short self-check that can be run before delivery.

## Design Invariants

These rules apply to every concrete style:

- Style is structure plus behavior, not only colors.
- Semantic roles beat decorative preference; do not compromise readability for ornament.
- Shared mechanics must stay reusable and style-neutral.
- Concrete styles must be substitutable through the same workflow.
- Identity assets require proportion-preserving placement.
- New styles should extend the framework, not fork the workflow.

## Quality Gate

Before delivery, verify alignment, spacing, hierarchy, text overflow, contrast, responsiveness, image distortion, decorative relevance, asset provenance, and style fidelity. If the artifact no longer reads as the selected concrete style, revise before final output.

## Bundled Resources

- `references/style_registry.md`: concrete-style registry and extension index.
- `references/style_contract.md`: formal interface, data-shape, and asset-provider contract.
- `references/style_template.md`: skeleton for adding new concrete style implementations.
- `references/design_mechanics.md`: shared same-family progression, style-owned asset interface rules, and surface texture rules.
- `references/seu_design_style.md`: concrete implementation for the SEU style.
- `references/renminbi_color_style.md`: concrete implementation for banknote-inspired RMB color rules.
- `references/chinese_traditional_color_style.md`: concrete implementation for Chinese traditional color systems.
- `assets/seu_design_style/`: SEU SVG identity assets copied from the UI Guide source.
- `assets/seu_design_style/ASSET_MANIFEST.md`: SEU asset-module manifest with roles, dimensions, ratios, and safe placement modes.
- `references/texture_provider.md`: shared raster-first `SurfaceTextureProvider` contract for low-opacity bottom-surface texture.
- `assets/transparent_textures/`: curated Transparent Textures PNG overlays, source download metadata, JSON index, and optional SVG wrapper adapters.
- `assets/transparent_textures/TEXTURE_MANIFEST.md`: texture-token manifest with source URLs, tile sizes, visual character, surface roles, opacity bounds, and placement rules.
