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
  provider: "none" | string;
  assetRoot: "none" | `assets/${string}/`;
  manifestFile?: string;
  indexFile?: string;
  defaultToken?: string;
  allowedTokens: string[];
  opacityRange: [number, number];
  allowedSurfaces: string[];
  forbiddenSurfaces: string[];
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

type TextureAssetFormat = "png" | "svg-wrapper" | string;

interface SurfaceProviderManifestItem {
  token: string;
  file: string;
  sourceUrl?: string;
  sourceFormat: string;
  width?: number;
  height?: number;
  sha256?: string;
  visualCharacter: string;
  recommendedRoles: string[];
  defaultOpacity: [number, number];
  safePlacement: "tile" | "panel" | "edge-band" | string;
}
```

## Self-Check Output Contract

Concrete style `Self-Check` sections should produce or simulate this shape before delivery:

```ts
const result: CheckResult = {
  ok: boolean,              // true only when no required fixes remain
  issues: string[],         // concrete visual, contract, asset, or readability problems
  requiredFixes: string[],  // changes required before final delivery
};
```

Use style-specific checks inside that shape. For example, SEU checks logo aspect ratios and institutional restraint; RMB checks non-counterfeit behavior; Chinese traditional color checks named-color and cultural-context fit.

## Substitutability Rules

- The template workflow should not special-case one style after resolution.
- If one style needs a new behavior, first add a method or optional interface here, then let every style either implement it or explicitly declare `none`.
- Concrete styles may have assets, no assets, or user-provided-only assets, but all must expose an `AssetPolicy`.
- Concrete styles must also expose a `SurfaceTexturePolicy`, even if it declares `provider: none`. Surface providers are optional substrate services, not identity assets.
- A style may enable a non-`none` surface provider only when every referenced provider file exists and has provenance documentation.
- A style may be brand-led, color-led, or motif-led; the workflow should still consume it through the same methods.
- Medium translation must cover PPT, web, app/dashboard, and static visual output, even if the style simply says to reuse layout/color rules for a medium.
