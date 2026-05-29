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

## Style-Owned Asset Interface

Shared mechanics do not provide a global ornament or texture library. Assets belong to concrete styles and must be selected through that style's `AssetPolicy`.

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
- If the selected style has no approved assets, rely on layout, typography, color progression, simple rules, and code-native geometry instead of downloading filler.

### SEU Example

`seu_design_style` exposes curated assets under `assets/seu_design_style/`. Its reference file names approved uses for logo marks, wordmarks, motto artwork, auditorium silhouettes/patterns, and pine motifs. Those files are the model for future style-owned asset interfaces.


## Shared Surface Texture Provider

Some artifacts need a subtle bottom-surface texture: paper grain, micro dots, quiet geometric noise, or graph-like backing. This is a framework-level utility, not a concrete style ornament library.

The shared provider lives under `assets/transparent_textures/` and is documented by `assets/transparent_textures/TEXTURE_MANIFEST.md` plus the machine-readable `texture_index.json`. Concrete styles opt in through `SurfaceTexturePolicy`; if a style does not opt in, the workflow should not apply a texture.

The provider is raster-first because Transparent Textures distributes transparent PNG tiles. `svg_wrappers/*.pattern.svg` exists only as an adapter for SVG-oriented import paths; the PNG remains the source of truth.

```ts
interface SurfaceTexturePolicy {
  provider: "transparent_textures" | "none";
  assetRoot: "assets/transparent_textures/" | "none";
  manifestFile?: "assets/transparent_textures/TEXTURE_MANIFEST.md";
  indexFile?: "assets/transparent_textures/texture_index.json";
  nativeFormat?: "png";
  allowedAdapterFormats?: ("png" | "svg-wrapper")[];
  defaultToken?: TextureToken;
  allowedTokens: TextureToken[];
  opacityRange: [number, number];
  allowedSurfaces: SurfaceRole[];
  forbiddenSurfaces: SurfaceRole[];
  fallbackPolicy: string;
}
```

### Texture Resolution Rules

- Treat textures as substrate, not motif. They should support surface depth while remaining visually secondary to content, color tokens, typography, and data.
- The selected concrete style decides which tokens are allowed. The base skill must not pick `old-map`, `honeycomb-light`, or any other token merely because it looks good.
- Apply textures below text and components, never as a foreground overlay.
- Use low opacity by default: 2-10% is the normal range. Stronger values require explicit user direction and a successful contrast check.
- Do not combine shared textures with official identity patterns on the same region unless the concrete style explicitly allows it.
- For PPT and PDF, use the native PNG tile and precompose it into a raster at the target canvas size. For web/app, repeat the original PNG tile and control strength with a separate opacity layer.
- For SVG-oriented pipelines, use `svg_wrappers/*.pattern.svg` only as an adapter. Do not treat it as true vector texture geometry.
- Turning texture off should still leave a complete design. Texture enriches the surface; it must not carry meaning.

### Suggested Style Defaults

| Style | Default token | Allowed tokens | Typical surfaces |
| --- | --- | --- | --- |
| `seu_design_style` | `dot-micro` | `dot-micro`, `diagonal-noise`, `graph-grid`, `honeycomb-light`, `paper-cream` | cover background, section background, data panel, chart backing |
| `renminbi_color_style` | `paper-cream` | `paper-cream`, `paper-fibers`, `diagonal-noise`, `graph-grid` | paper-like full backgrounds, metric panels, value proposition pages |
| `chinese_traditional_color_style` | `paper-fibers` | `paper-cream`, `paper-fibers`, `old-map`, `escher-geometry`, `diagonal-noise` | editorial backgrounds, museum pages, section pages, edge bands |

## QA Checklist

- The chosen color progression has at least four useful steps, not just a primary and one pale tint.
- Non-primary emphasis uses support colors before repeating the primary.
- Broad washes use enough contrast with text.
- Asset role is resolved through the selected style before placement. If a manifest exists, use it to choose the file and compute the contain box.
- Texture role is resolved through the selected style's `SurfaceTexturePolicy`; shared textures are applied only as low-opacity substrate layers.
- Asset opacity, scale, and crop support content instead of filling empty space.
- No generated or downloaded asset imitates official identity assets, legal tender, protected seals, or copyrighted object scans.
- Texture opacity and placement preserve text contrast and data readability.
- Use only the active style's approved assets; avoid mixing unrelated asset families.
