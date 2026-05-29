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

- Choose colors from the style's source palette first. Do not invent extra tints when the source palette already contains usable neighbors.
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
4. If assets are unavailable, use the active style's fallback language: code-native geometry, typography, color blocks, charts, diagrams, rules, or lawful user-provided assets.
5. Add anti-monotony checks to the final quality gate; variety must not override readability, provenance, brand safety, or style anti-goals.

## Style-Owned Asset Interface

Shared mechanics do not provide a global ornament or texture library. Assets belong to concrete styles and must be selected through that style's `AssetPolicy`. Recommended external sources are maintained at the skill level in `SKILL.md`; imported reusable files must still become style-owned manifest entries before use.

Think of `AssetPolicy` as an import interface. The base skill never reaches directly into `assets/`; it asks the selected concrete style which asset module is available and what each exported asset is allowed to do.

```ts
interface AssetPolicy {
  assetRoot: `assets/${styleName}/` | "none";
  importMode: "style-owned" | "none" | "user-provided-only";
  manifestFile?: string;
  availableAssets: Record<string, AssetRole[]> | "none";
  placementRules: PlacementRule[];
  distortionRules: DistortionRule[];
  fallbackPolicy: string;
}
```

### Asset Manifest Contract

When `assetRoot` is not `none`, the style should provide either a manifest section in its reference file or a separate `ASSET_MANIFEST.md` under its asset folder.

A manifest should list: `file`, `role`, intrinsic width/height or ratio, color mode, safe placement mode, and notes. This makes the style behave like a typed import module rather than a loose folder of images.

### Rules

- Use style-owned assets only from the active style folder, for example `assets/seu_design_style/` when `seu_design_style` is selected.
- Do not assume files from another style are interchangeable. SEU auditorium and pine assets should not silently become RMB or Chinese-traditional motifs.
- Preserve intrinsic aspect ratio for all SVG and raster assets.
- Use contain-style placement for identity marks, wordmarks, motto artwork, silhouettes, and informative motifs.
- Use low-opacity or repeated motifs only when the concrete style explicitly allows that behavior.
- If the selected style has no approved assets, rely on layout, typography, color progression, simple rules, and code-native geometry instead of downloading filler; download external assets only when the task specifically needs them and the skill-level acquisition rules can be satisfied.

### SEU Example

`seu_design_style` exposes curated assets under `assets/seu_design_style/`. `renminbi_color_style` and `chinese_traditional_color_style` currently expose no bundled assets and rely on code-native geometry, generated vectors, user-provided assets, or task-local Pixabay/Iconfont assets with provenance. Future reusable style-owned assets must be placed directly under `assets/<style_name>/` with a manifest role, safe placement mode, provenance/source note, and forbidden-use boundary.


## Style Preview Mechanics

Use the preview phase to make style choices visible before committing to a full PPT, web page, app screen, dashboard, or static visual when preview is requested or auto-mode detects ambiguity, high stakes, public-facing delivery, brand sensitivity, or high regeneration cost. The preview is not the final artifact; it is a compact decision surface for user approval when approval is needed.

Default preview surface:

- `canvas`: use the target medium ratio when known; otherwise use a 16:9 combined style board.
- `style header`: style name, target medium, content goal, and selected defaults.
- `palette strip`: primary, support, wash, neutral, text, and accent tokens with labels.
- `typography sample`: title, subtitle, body, caption, and numeral sample.
- `component sample`: one card, one table/chart fragment, and one button/tag/navigation state when relevant.
- `surface sample`: background, panel, edge band, and texture token or texture-off state.
- `asset or motif sample`: only assets, motifs, or generated geometry allowed by the active style's policy.

Preview option rules:

- Keep the same preview surface while swapping options so users compare like-for-like.
- Expose only options that are valid under the active style's palette, asset policy, surface texture policy, and modifier compatibility rules.
- Include a safe off/fallback option for texture or motif choices when disabling them still preserves the style.
- Do not browse provider assets directly; texture options must be declared by the style's `SurfaceTexturePolicy.allowedTokens`.
- For ordinary direct artifact requests, create an internal `StyleLock` from style defaults and proceed without stopping for approval.
- Do not produce the complete deck, website, app, or dashboard before approval when explicit preview is requested or auto-mode decides approval is needed.
- The final artifact must match the approved or internally locked palette family, texture token or off state, layout density, motif level, and asset emphasis.

## Surface Texture Extension Point

The canonical shared surface texture provider is `transparent_textures`, sourced from Transparent Textures (`https://www.transparenttextures.com/`) for high-quality tileable texture resources. A curated provider is bundled under `assets/transparent_textures/` with SVG wrappers, `TEXTURE_MANIFEST.md`, `texture_index.json`, provenance notes, and validator checks. Other recommended material sources belong to the skill-level source list in `SKILL.md`; they are not shared providers until files are curated, documented, indexed, and validator-supported.

Concrete styles may declare `provider: transparent_textures` only when every token in their `SurfaceTexturePolicy` exists in the provider index and remains a neutral substrate service, not a global ornament library.

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
  forbiddenSurfaces: string[];
  fallbackPolicy: string;
}
```

### Transparent Textures Provider Rules

- Add actual wrapper/source files and metadata before enabling new `transparent_textures` tokens in any concrete style.
- Source current shared texture files from `https://www.transparenttextures.com/` and record the original pattern name, creator attribution when available, download/source URL, license or terms note, native format, dimensions when known, checksum, safe placement, and allowed surfaces. For future texture candidates discovered through any recommended source, first add them as style-owned or project assets with provenance; promote them to a shared provider only after adding an index, manifest, checksums, and validator support.
- Keep textures below content; never use them as motifs, official marks, or semantic data encodings.
- Turning texture off must still leave a complete design. Texture enriches the surface; it must not carry meaning.
- If texture weakens contrast or data readability, disable it and preserve style through color, typography, layout, and approved style-owned assets.

## QA Checklist

- The chosen color progression has at least four useful steps, not just a primary and one pale tint.
- Non-primary emphasis uses support colors before repeating the primary.
- Broad washes use enough contrast with text.
- Asset role is resolved through the selected style before placement. If a manifest exists, use it to choose the file and compute the contain box.
- Surface texture is used only when the selected style declares an available provider and every referenced provider file exists.
- Asset opacity, scale, and crop support content instead of filling empty space.
- No generated or downloaded asset imitates official identity assets, legal tender, protected seals, or copyrighted object scans.
- If surface texture is disabled or unavailable, the design still reads clearly through color, typography, layout, and approved assets.
- Use only the active style's approved assets; avoid mixing unrelated asset families.
