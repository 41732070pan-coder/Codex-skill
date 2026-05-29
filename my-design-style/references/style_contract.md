# Style Contract

This file is the formal interface layer for `my-design-style`. `SKILL.md` owns the template workflow; concrete style files implement this contract through stable sections.

## Core Data Shapes

```ts
type TargetMedium = "ppt" | "web" | "app" | "dashboard" | "document_visual" | "static_visual" | "design_template";

type StyleName = "seu_design_style" | "renminbi_color_style" | "chinese_traditional_color_style" | string;

interface DesignRequest {
  medium: TargetMedium;
  contentGoal: "explain" | "persuade" | "compare" | "report" | "present" | "brand" | "sell" | "teach" | string;
  audience?: string;
  context?: string;
  explicitStyle?: StyleName;
  constraints: {
    dimensions?: string;
    platform?: string;
    accessibility?: string[];
    requiredAssets?: string[];
    outputFormat?: string;
    brandRequirements?: string[];
  };
}

interface StyleResolution {
  styleName: StyleName;
  referenceFile: `references/${string}.md`;
  confidence: "explicit" | "strong" | "medium" | "weak";
  reason: string;
  askIfAmbiguous: boolean;
}

interface CheckResult {
  ok: boolean;
  issues: string[];
  requiredFixes: string[];
}
```

## Required Interfaces

A concrete style is valid only if its reference file supplies evidence for every interface below.

```ts
interface TriggerMatcher {
  names: string[];
  aliases: string[];
  domainCues: string[];
  defaultPolicy: string;
  match(request: DesignRequest): StyleResolution | null;
}

interface DesignIntentProvider {
  getDesignIntent(): string;
  getAntiGoals(): string[];
}

interface PaletteProvider {
  getColorTokens(): Record<string, { hex: string; role: string }>;
  getSeriesCards(): SeriesColorCard[];
  getSameFamilyProgressions(): SameFamilyProgression[];
}

interface TypographyProvider {
  getTypographySystem(): {
    primaryFonts: string[];
    accentFonts?: string[];
    hierarchyRules: string[];
    fallbackRules: string[];
  };
}

interface LayoutSystem {
  getLayoutRules(): {
    grid: string[];
    spacing: string[];
    density: string;
    hierarchy: string[];
    compositionRules: string[];
  };
}

interface ComponentTranslator {
  translatePPT(): MediumRules;
  translateWeb(): MediumRules;
  translateAppDashboard(): MediumRules;
  translateStaticVisual(): MediumRules;
}

interface AssetPolicy {
  assetRoot: `assets/${string}/` | "none";
  importMode: "style-owned" | "none" | "user-provided-only";
  manifestFile?: string;
  availableAssets: Record<string, AssetRole[]> | "none";
  placementRules: string[];
  distortionRules: string[];
  fallbackPolicy: string;
}

interface SurfaceTexturePolicy {
  provider: "transparent_textures" | "none";
  assetRoot: "assets/transparent_textures/" | "none";
  manifestFile?: "assets/transparent_textures/TEXTURE_MANIFEST.md";
  defaultToken?: TextureToken;
  allowedTokens: TextureToken[];
  opacityRange: [number, number];
  allowedSurfaces: SurfaceRole[];
  forbiddenSurfaces: SurfaceRole[];
  fallbackPolicy: string;
}

interface QualityGate {
  selfCheck(outputDescription: string): CheckResult;
}
```

## Asset Provider Contract

Treat each style asset folder as a module. The base workflow must not browse `assets/` directly and choose arbitrary files; it must ask the active concrete style what that module exports.

```ts
interface AssetProvider {
  styleName: StyleName;
  root: `assets/${string}/`;
  manifest: AssetManifestItem[];
  resolve(role: AssetRole, medium: TargetMedium): AssetManifestItem[];
}

interface AssetManifestItem {
  file: string;
  roles: AssetRole[];
  intrinsicRatio?: number;
  width?: number;
  height?: number;
  colorMode: "color" | "mono" | "mixed" | "unknown";
  safePlacement: "contain" | "repeatable" | "crop-allowed";
  notes?: string;
}

type AssetRole =
  | "identity-mark"
  | "wordmark"
  | "logo-lockup"
  | "motto"
  | "building-silhouette"
  | "pattern"
  | "color-card"
  | "botanical-motif"
  | "decorative-rule"
  | "background-texture";

type TextureAssetFormat = "png" | "svg-wrapper";

interface TransparentTextureProvider {
  providerName: "transparent_textures";
  assetRoot: "assets/transparent_textures/";
  manifestFile: "assets/transparent_textures/TEXTURE_MANIFEST.md";
  indexFile: "assets/transparent_textures/texture_index.json";
  nativeFormat: "png";
  adapterFormats: ["svg-wrapper"];
  resolve(token: TextureToken, medium: TargetMedium, preferredFormat?: TextureAssetFormat): TextureManifestItem;
}

interface TextureManifestItem {
  token: TextureToken;
  file: string;              // native PNG tile, source of truth
  svgWrapper?: string;       // optional adapter, not true vectorization
  sourceUrl?: string;
  sourceFormat: "png";
  width: number;
  height: number;
  bytes?: number;
  sha256?: string;
  visualCharacter: string;
  recommendedRoles: SurfaceRole[];
  defaultOpacity: [number, number];
  safePlacement: "tile" | "panel" | "edge-band";
}

type TextureToken =
  | "paper-cream"
  | "paper-fibers"
  | "dot-micro"
  | "diagonal-noise"
  | "honeycomb-light"
  | "graph-grid"
  | "escher-geometry"
  | "old-map";

type SurfaceRole =
  | "full-background"
  | "cover-background"
  | "section-background"
  | "data-panel"
  | "chart-backing"
  | "sidebar"
  | "edge-band"
  | "callout-card";
```

## Substitutability Rules

- The template workflow should not special-case one style after resolution.
- If one style needs a new behavior, first add a method or optional interface here, then let every style either implement it or explicitly declare `none`.
- Concrete styles may have assets, no assets, or user-provided-only assets, but all must expose an `AssetPolicy`.
- Concrete styles must also expose a `SurfaceTexturePolicy`, even if it declares `provider: none`. Shared textures are optional substrate services, not identity assets.

- Transparent Textures use a raster-first contract: `sourceFormat: png`; `svg-wrapper` is only an adapter boundary and must not be treated as native vector artwork.
- A style may be brand-led, color-led, or motif-led; the workflow should still consume it through the same methods.
- Medium translation must cover PPT, web, app/dashboard, and static visual output, even if the style simply says to reuse layout/color rules for a medium.
