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


## Visual Rhythm Mechanics

Use this shared mechanic when a target artifact has multiple slides, screens, sections, or dense content blocks. The concrete style owns the specific motifs and allowed fallbacks; this mechanic only defines the neutral planning pattern.

1. Create an archetype sequence before detailed layout. Mix high-impact, structured, dense, and visual surfaces instead of repeating one skeleton.
2. Assign one non-body-text visual anchor to every slide/screen/major section. Anchors can be informational diagrams, charts, tables, swatches, imagery, structural rails, label frames, texture bands, or approved motifs.
3. Rotate visual treatments across the artifact: scale, column count, anchor side, motif type, texture on/off, and density.
4. Build an asset-rich rhythm by default. For a normal multi-slide deck, website, app mockup, dashboard, or static visual, use about 5-10 distinct assets or asset roles across the artifact unless the user asks for a wireframe, the artifact is very small, or a concrete safety/accessibility blocker exists.
5. When internet access is available and safe for the task, search relevant material sources as part of design exploration; compare sourced candidates with visible runtime assets, shared texture providers, generated bitmap/vector assets, code-native geometry, typography, charts, diagrams, rules, and user-provided assets before choosing the least monotonous style-faithful option.
6. Add variation checks to the final quality gate; variety should preserve readability, provenance, brand safety, and style safety boundaries.

## Style-Owned Asset Interface

Shared mechanics do not provide a global ornament or texture library. Assets belong to concrete styles and must be selected through that style's `AssetPolicy`. Recommended external sources are maintained at the skill level in `SKILL.md`; imported reusable files need provenance, but file-level state stays inside the opaque asset bundle or task documentation.

Think of `AssetPolicy` as an import interface. The base skill asks the selected concrete style for stable handles, allowed roles, and fallback behavior, then inspects the visible runtime asset boundary while building the actual artifact. Inventory stays out of framework references, but generation should not pretend visible assets are unavailable.

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

- `defaultMode`: use `asset-rich` for ordinary personal/internal artifacts.
- `targetDistinctAssets`: use `5-10` for normal decks, websites, apps, dashboards, and static visuals.
- `selectedAssets`: include style-owned files, shared provider textures, user-provided files, generated assets, and sourced no-login/no-paywall materials that fit the artifact.
- `shapeOnlyExceptionReason`: required when the final artifact uses no embedded assets or no meaningful asset roles.
- `checks`: include aspect ratio, placement role, source/path note, and readability impact.

Do not count ordinary rectangles, lines, arrows, text boxes, table cells, or routine chart primitives as assets. Code-native geometry is still useful for structure, diagrams, charts, and simple original ornament, but it cannot be the global default substitute for available image, motif, icon, texture, or identity assets.

### Opaque Asset Boundary Contract

Skill-level references may declare abstract asset handles, allowed roles, placement rules, and fallback behavior while file inventories stay in manifests or task-local documentation.

Every concrete style must still maintain:

- `assets/<style_name>/`
- `assets/<style_name>/ASSET_MANIFEST.md`

File-level provenance, dimensions, checksums, and source notes belong inside the asset bundle or task-local documentation. The framework treats those details as runtime data that users may replace without editing the skill instructions, but the boundary directory itself is a required structural invariant checked by `validate_styles.py`.

### Rules

- Use assets exposed by the active style's `AssetPolicy`, and inspect visible files in that style's asset boundary when producing a real artifact.
- For personal/non-commercial work, visible files in the active style boundary are usable by default when the role fits the content; stricter rights review is reserved for public/commercial release, sensitive identity use, legal/security-document-adjacent work, or unclear external sources.
- Avoid global `asset-off`, `no external assets`, or shape-only choices unless an exception is explicitly requested or recorded in the `AssetUsePlan`.
- Use assets exposed by the active style's `AssetPolicy`, or document another style's asset boundary as an intentional hybrid/user-provided source.
- Treat files from another style as a deliberate hybrid or user-provided source, not as automatic shared clip art.
- Preserve intrinsic aspect ratio for all SVG and raster assets that the active policy exports.
- Use contain-style placement for identity marks, wordmarks, motto artwork, silhouettes, and informative motifs.
- Use low-opacity or repeated motifs only when the concrete style explicitly allows that behavior.
- Use network discovery proactively for task-relevant material comparison when allowed; runtime assets, sourced candidates, generated bitmap/vector assets, user-provided assets, and code-native geometry should be weighed together for style fidelity, semantic fit, provenance safety, and variation value.


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
- The final artifact must match the approved or internally locked palette family, texture token or off state, layout density, motif level, and asset emphasis. If the lock produces fewer than 5 distinct assets or asset roles for a normal non-wireframe artifact, record the exception reason before delivery.

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

- Keep provider file inventories, source records, checksums, and wrapper metadata inside the provider bundle or task-local documentation rather than framework references.
- Keep textures below content; use them as surface character rather than official marks or semantic data encodings.
- Turning texture off should still leave a complete design. Texture enriches the surface; meaning should come from color, type, layout, imagery, and data.
- If texture weakens contrast or data readability, disable it locally and preserve style through color, typography, layout, and other visible assets.

## QA Checklist

- The chosen color progression has at least four useful steps, not just a primary and one pale tint.
- Non-primary emphasis uses support colors before repeating the primary.
- Broad washes use enough contrast with text.
- Asset role is resolved through the selected style before placement. Use runtime metadata exposed by the active policy to choose handles and compute contain boxes.
- Normal visual artifacts use about 5-10 distinct asset roles or files unless an exception is recorded.
- Surface texture is used when the selected style declares a provider handle and fallback behavior; provider file existence stays outside framework validation.
- Asset opacity, scale, and crop support content instead of filling empty space.
- Generated or downloaded assets stay original or properly licensed when they evoke official identity systems, legal tender, protected seals, or copyrighted object scans intended for public/commercial release; personal/internal drafts may use visible assets with source notes unless the task is sensitive or misleading.
- If surface texture is disabled or unavailable, the design still reads clearly through color, typography, layout, and other visible assets.
- Use runtime assets exposed by the active style policy, or document intentional hybrid/user-provided asset families.
- Reject shape-only delivery as incomplete when relevant visible assets were available and no exception was recorded.
