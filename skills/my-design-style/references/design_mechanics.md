# Shared Design Mechanics

Use this file for design mechanisms that should work across every `my-design-style` family. Named style files choose specific colors, type, layout rhythm, and asset preferences; this file defines the reusable construction rules.

## Same-Family Color Progression

A style should not stop at one primary color plus unrelated accents. When a user selects a hue family such as red, green, blue, yellow, purple, SEU green, or RMB 100-yuan red, build a progression that can carry hierarchy without shouting.

| Role | Purpose | Typical Use |
| --- | --- | --- |
| `primary` | The identifying color of the family. | Main title, hero metric, primary series, active section. |
| `support-strong` | Neighboring deep or saturated color. | Secondary emphasis, section marker, selected state, contrast chip. |
| `support-mid` | Middle value in the same family. | Data companion, comparison mark, panel heading, tag fill. |
| `support-soft` | Softer or lower-saturation family color. | Gentle callout, inactive highlight, chart background mark. |
| `wash` | Pale family color. | Background wash, transition panel, selected row, soft surface. |
| `muted-bridge` | Grayed, browned, or cooled family bridge. | Metadata, divider, transition between family and neutral base. |

### Rules

- Choose colors from the style's source palette first, then add extra tints only when they serve a clear medium, contrast, or mood need.
- The progression should feel like one family under different pressure: not a rainbow and not six unrelated accents.
- Use `primary` sparingly. Most emphasis should use `support-strong`, `support-mid`, or `support-soft` so the page can show hierarchy without overusing the main color.
- Use `wash` for broad surfaces only when text contrast remains strong.
- Use `muted-bridge` to move from color into neutral UI, paper, chart axes, borders, and captions.
- In charts, one family can encode a sequence, confidence level, recency, amount, or depth; use clearly different lightness/saturation steps.
- In UI, map progression roles to states: active = primary/support-strong, hover = support-mid, selected row = wash, disabled = muted-bridge plus neutral text.

### Example Card Shape

```text
Family: Red / 100-yuan / Rouge
primary:         #9D2933
support-strong:  #BE002F
support-mid:     #DB5A6B
support-soft:    #EF7A82
wash:            #FFB3A7
muted-bridge:    #B36D61
neutral-base:    #FFFBF0 / #161823
```


## Default Series Selection

Use this mechanic whenever a concrete style must choose a palette series, denomination family, or palette recipe and the user did **not** name one. The goal is "varied by default": repeated runs of the same style should explore its full range instead of collapsing onto one habitual card.
Build a `DefaultSeriesSelection` and pick with genuine variation:

1. `candidates`: start from the active style's working series cards, denomination families, or palette recipes. Exclude the neutral "use only when no family should lead" fallback from the candidate pool unless every expressive card is genuinely unsuitable.
2. `fitFilter`: keep only candidates whose documented `Use` fits the content goal, subject, medium, audience, environment, and any brand, accessibility, or platform constraint. Preserve semantic color meaning (risk/value reds, trust greens, premium purples, etc.) so variation never overrides a meaningful signal.
3. `overrides`: an explicit user palette choice, a strong domain or brand cue, a hard accessibility/contrast limit, and any persisted user preference always win over randomization. Randomize only across the remaining genuinely-equivalent candidates.
4. `variedPick`: from the filtered pool, choose one candidate with weighted randomness rather than always the first, most familiar, or most "default-feeling" one. Weight by fit strength, and when more than one candidate qualifies, avoid repeating the immediately previous default for the same style.
5. `lockAndDisclose`: record the chosen series/recipe in `StyleLock`, and note in the final delivery that it was an auto-varied default so the user can pin a fixed series next time.

Scope rules:

- Apply variation to palette/series defaults only. Keep deterministic style-safety defaults (texture token, opacity range, layout density, motif restraint, asset-rich coverage, identity invariants such as a brand's required structure color) unless the user opts into varying them too.
- If the filtered pool ends up empty, fall back to the style's documented neutral fallback card and say so.
- Variation must never weaken contrast, accessibility, or the style's hard identity invariants; those are filters applied before the pick, not things the pick can break.

### Selection Shape

```ts
interface DefaultSeriesSelection {
  candidates: string[];          // working cards / denomination families / recipes
  fitFilter: string[];           // content, medium, audience, environment, constraints applied
  overrides: string[];           // explicit choice, strong cue, hard limits, saved preference
  variedPick: string;            // chosen card/recipe
  reason: string;                // why it fits + that it was an auto-varied default
}
```


## Visual Rhythm Mechanics

Use this shared mechanic when a target artifact has multiple slides, screens, sections, or dense content blocks. The concrete style owns the specific motifs and allowed fallbacks; this mechanic only defines the neutral planning pattern.

1. Create an archetype sequence before detailed layout. Mix high-impact, structured, dense, and visual surfaces instead of repeating one skeleton.
2. Assign one non-body-text visual anchor to every slide/screen/major section. Anchors can be informational diagrams, charts, tables, swatches, imagery, structural rails, label frames, texture bands, or approved motifs.
3. Rotate visual treatments across the artifact: scale, column count, anchor side, motif type, texture on/off, and density.
4. Build an asset-rich rhythm by default. For a normal multi-slide deck, website, app mockup, dashboard, or static visual, use about 5-10 distinct assets or asset roles across the artifact unless the user asks for a wireframe or the artifact is very small.
5. When internet access is available, search relevant material sources as part of design exploration; compare sourced candidates with visible runtime assets, shared texture providers, generated bitmap/vector assets, code-native geometry, typography, charts, diagrams, rules, and user-provided assets before choosing the least monotonous style-faithful option.
6. Add variation checks to the final quality gate; variety should preserve readability and style fidelity.

## Style-Owned Asset Interface

Shared mechanics do not provide a global ornament or texture library. Assets belong to concrete styles and must be selected through that style's `AssetPolicy`. Recommended external sources are maintained at the skill level in `SKILL.md`.

Think of `AssetPolicy` as an import interface. The base skill asks the selected concrete style for stable handles, allowed roles, and fallback behavior, then inspects the visible runtime asset boundary while building the actual artifact. Generation should not pretend visible assets are unavailable, and an empty boundary means assets are downloaded or generated at runtime.

```ts
interface AssetPolicy {
  assetRoot: `assets/${styleName}/`;
  importMode: "style-owned" | "user-provided-only" | "style-owned-visible" | "personal-visible-assets";
  manifestFile?: string;
  availableAssets: Record<string, AssetRole[]> | "none";
  placementRules: PlacementRule[];
  distortionRules: DistortionRule[];
  fallbackPolicy: string;
}
```

### Default Asset Use Plan

For concrete visual output, create an `AssetUsePlan` before detailed layout:

- `defaultMode`: use `asset-rich` for every visual artifact.
- `targetDistinctAssets`: use `5-10` for normal decks, websites, apps, dashboards, and static visuals.
- `selectedAssets`: include style-owned files, shared provider textures, user-provided files, generated assets, and network-sourced materials that fit the artifact.
- `checks`: include aspect ratio, placement role, and readability impact.

Do not count ordinary rectangles, lines, arrows, text boxes, table cells, or routine chart primitives as assets. Code-native geometry is still useful for structure, diagrams, charts, and simple original ornament, but it cannot be the global default substitute for available image, motif, icon, texture, or identity assets. When the visible inventory is thin, download or generate assets to reach the target range.

### Richness And Restraint Balance

Beauty comes from purposeful coverage plus breathing room, not from maximizing asset count. The 5-10 range is a guide for variety, not a quota to fill.

- Treat whitespace as an active design element: generous margins, clear hierarchy, and quiet zones make assets and content read as intentional rather than crowded.
- Each asset must earn a semantic or structural role. Drop any asset that duplicates an existing anchor, fights hierarchy, weakens contrast or legibility, or only fills space — asset-rich is never asset-cluttered.
- Restrained or minimal styles may sit at the low end of the range and lean on color, type, layout, and a few high-value anchors; restraint is a valid expressive choice, not an asset-coverage failure, as long as no surface is left empty or monotonous.
- The tension to resolve per surface is "enough variety to avoid monotony" versus "enough calm to stay readable and elegant"; let the content goal, density, and style identity decide where each surface lands.

### Opaque Asset Boundary Contract

Skill-level references may declare abstract asset handles, allowed roles, placement rules, and fallback behavior while file inventories stay in manifests or task-local documentation.

Every concrete style must still maintain:

- `assets/<style_name>/`
- `assets/<style_name>/ASSET_MANIFEST.md`

The boundary directory is a required structural invariant checked by `validate_styles.py`. An empty boundary is valid and means "download or generate assets at runtime", not "ship without assets".

### Rules

- Use assets exposed by the active style's `AssetPolicy`, and inspect visible files in that style's asset boundary when producing a real artifact.
- Visible files in the active style boundary are usable by default when the role fits the content.
- Avoid global `asset-off`, `no external assets`, or shape-only choices unless the user explicitly asks for a wireframe/data diagram.
- Use assets exposed by the active style's `AssetPolicy`, another style's asset boundary, or network-sourced files as a freely combined pool.
- When a style's visible inventory is empty or thin, download task-relevant assets from the network or generate vectors/bitmaps before falling back to shape-only.
- Preserve intrinsic aspect ratio for all SVG and raster assets that the active policy exports.
- Use contain-style placement for identity marks, wordmarks, motto artwork, silhouettes, and informative motifs.
- Use low-opacity or repeated motifs only when the concrete style explicitly allows that behavior.
- Use network discovery proactively for task-relevant material comparison; runtime assets, sourced candidates, generated bitmap/vector assets, user-provided assets, and code-native geometry should be weighed together for style fidelity, semantic fit, and variation value.

### Asset Format Conversion And Transparency

Some target media cannot embed vector assets directly. For example, `python-pptx` cannot insert SVG through `add_picture`, and other raster-only embedders behave the same way. Treat "the medium does not support SVG" as a conversion task, not a reason to drop the asset and fall back to code-native shapes.

- When the medium cannot embed a vector asset, rasterize it first with a vector renderer such as `cairosvg`, Inkscape (`inkscape --export-type=png`), or `svglib` + `reportlab`. Export `PNG` for raster embedders, or `EMF` when the medium can import editable vector.
- Render with an alpha channel (`RGBA`), never flatten to `RGB`. Most motif, ornament, icon, border, and identity assets rely on a transparent background; flattening injects an opaque, usually white, box that clashes with colored or textured surfaces and looks pasted-on.
- After insertion, verify the asset on a colored or textured surface that there is no visible white or opaque rectangle around it. If one appears, re-export as RGBA, or trim/key out the background before reuse.
- Export at enough resolution for the placement box (about 2x the target pixel size) so edges stay crisp after scaling, and preserve the intrinsic aspect ratio during both conversion and placement.
- Keep the conversion reproducible: convert at build time from the source vector instead of committing only a flattened bitmap, and keep reusable converted files inside the style's `assets/<style_name>/` boundary or a build cache.


## Style Preview Mechanics

Use the preview phase to make style choices visible before committing to a full PPT, web page, app screen, dashboard, or static visual when preview is requested or auto-mode detects ambiguity, high stakes, public-facing delivery, brand sensitivity, or high regeneration cost. The preview is not the final artifact; it is a compact decision surface for user approval when approval is needed.

Default preview surface:

- `canvas`: use the target medium ratio when known; otherwise use a 16:9 combined style board.
- `style header`: style name, target medium, content goal, and selected defaults.
- `palette strip`: primary, support, wash, neutral, text, and accent tokens with labels.
- `typography sample`: title, subtitle, body, caption, and numeral sample.
- `component sample`: one card, one table/chart fragment, and one button/tag/navigation state when relevant.
- `surface sample`: background, panel, edge band, and texture token or texture-off state.
- `asset or motif sample`: visible style assets, shared provider textures, user-provided files, generated assets, or sourced candidates allowed by the active style's policy and task context.

Preview option rules:

- Keep the same preview surface while swapping options so users compare like-for-like.
- Expose only options that are valid under the active style's palette, asset policy, surface texture policy, and modifier compatibility rules.
- Include an off/fallback option for local texture or motif choices when disabling them still preserves the style, but do not make all assets off by default for a normal visual artifact.
- Use texture options declared by the style's `SurfaceTexturePolicy` handles and backed by runtime fallback behavior.
- For ordinary direct artifact requests, create an internal `StyleLock` from style defaults and proceed without stopping for approval.
- When explicit preview approval is requested or auto-mode decides approval is needed, use the preview as the decision surface before committing to the complete deck, website, app, or dashboard.
- The final artifact must match the approved or internally locked palette family, texture token or off state, layout density, motif level, and asset emphasis. Aim for 5-10 distinct assets or asset roles in a normal non-wireframe artifact; if the locked defaults produce fewer, download or generate assets to reach that range.

## Surface Texture Extension Point

Shared surface providers are optional texture services exposed through `SurfaceTexturePolicy` handles. Provider internals under `assets/` are opaque to the framework; style documents may name provider handles and tokens while inventory/completeness details stay in manifests or task-local documentation.

Concrete styles may declare a provider only as a neutral substrate service, not a global ornament library, and must provide fallback behavior for cases where the runtime bundle differs from the author's local bundle.

```ts
interface SurfaceTexturePolicy {
  provider: "none" | "transparent_textures";
  assetRoot: "none" | `assets/${string}/`;
  manifestFile?: string;
  indexFile?: string;
  provenanceFile?: string;
  defaultToken?: string;
  allowedTokens: string[];
  opacityRange: [number, number];
  allowedSurfaces: string[];
  protectedSurfaces: string[];
  fallbackPolicy: string;
}
```

### Surface Provider Rules

- Keep provider file inventories and wrapper metadata inside the provider bundle or task-local documentation rather than framework references.
- Keep textures below content; use them as surface character rather than semantic data encodings.
- Turning texture off should still leave a complete design. Texture enriches the surface; meaning should come from color, type, layout, imagery, and data.
- If texture weakens contrast or data readability, disable it locally and preserve style through color, typography, layout, and other visible assets.

## QA Checklist

- The chosen color progression has at least four useful steps, not just a primary and one pale tint.
- Non-primary emphasis uses support colors before repeating the primary.
- Broad washes use enough contrast with text.
- Asset role is resolved through the selected style before placement. Use runtime metadata exposed by the active policy to choose handles and compute contain boxes.
- Surface texture is used when the selected style declares a provider handle and fallback behavior; provider file existence stays outside framework validation.
- Asset opacity, scale, and crop support content instead of filling empty space.
- If surface texture is disabled or unavailable, the design still reads clearly through color, typography, layout, and other visible assets.
- Use runtime assets exposed by the active style policy, other style boundaries, network-sourced files, generated assets, or user-provided files as a freely combined pool.
- Reject shape-only delivery as incomplete when relevant assets were available or could be downloaded/generated, and the user did not ask for a wireframe.
- Vector assets the medium cannot embed (for example SVG in `python-pptx`) are rasterized to RGBA `PNG`/`EMF` with transparency preserved, not dropped; confirm no unwanted white/opaque box appears on colored or textured surfaces.
- Produce an `AssetUseCheck` (see `style_contract.md`) as a delivery output and pass it through the quality gate: it records the distinct-asset count against the 5-10 target, the selected assets and their roles, and transparency, aspect-ratio, readability, and semantic-relevance quality flags. Resolve its `requiredFixes` before delivery.
