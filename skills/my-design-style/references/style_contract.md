# Style Contract

This file is the formal interface layer for `my-design-style`. `SKILL.md` owns the template workflow; concrete style files implement the abstract `DesignStyleBase` contract through stable sections. Provider interfaces below are helper facets of that base class, not separate style types.

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
  modifiers?: StyleModifier[];
  previewMode?: "required" | "skip" | "auto";
  previewConstraints?: {
    imageSize?: string;
    sampleContent?: string;
    maxOptionsPerGroup?: number;
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

// See `style_modifier_contract.md` for the full modifier contract.
interface StyleModifier {
  id: string;
  target: "palette" | "motif" | "texture" | "layout" | "mood" | "asset";
  operation: "add" | "replace" | "increase" | "decrease" | "tint";
  priority: "hard" | "soft";
  intensity?: "subtle" | "balanced" | "expressive";
  source?: "style-owned" | "user-provided" | "generated-vector" | "shared-provider" | "code-native" | "none";
  value: string | Record<string, unknown>;
  compatibilityRules: string[];
  selfCheckRules?: string[];
}

interface ComposedStylePlan {
  baseStyle: StyleName;
  modifiers: StyleModifier[];
  acceptedChanges: string[];
  reconciledChanges: string[];
  palettePlan?: Record<string, unknown>;
  motifPlan?: Record<string, unknown>;
  assetPlan?: Record<string, unknown>;
  assetUsePlan?: AssetUsePlan;
  visualRhythmPlan?: VisualRhythmPlan;
  previewPlan?: StylePreviewPlan;
  selfCheckPlan: string[];
}

interface StylePreviewPlan {
  baseStyle: StyleName;
  medium: TargetMedium;
  previewMode: "required" | "skip" | "auto";
  previewSurface: "style-board" | "artifact-sample" | "combined" | string;
  previewPrompt: string;
  selectedDefaults: Record<string, string>;
  optionSets: StyleOptionSet[];
  visualRhythmPlan?: VisualRhythmPlan;
  generationBoundary: string;
  selfCheckPlan: string[];
}

interface StyleOptionSet {
  id: string;
  target: "palette" | "texture" | "layout" | "mood" | "asset" | "motif" | string;
  label: string;
  defaultOptionId: string;
  options: StyleOption[];
  compatibilityRules: string[];
}

interface StyleOption {
  id: string;
  label: string;
  value: string | Record<string, unknown>;
  previewImpact: string;
  safetyNotes: string[];
}

interface StyleLock {
  approved: boolean;
  approvedPreviewId?: string;
  baseStyle: StyleName;
  medium: TargetMedium;
  selectedOptions: Record<string, string>;
  acceptedModifiers: string[];
  reconciledChanges: string[];
  lockedDecisions: Record<string, unknown>;
}

interface VisualRhythmPlan {
  rhythmScope: "single-surface" | "multi-slide-deck" | "multi-screen-flow" | "long-page" | string;
  archetypeSequence: string[];
  visualAnchors: Array<{ surface: string; anchor: string; role: "informational" | "structural" | "decorative" | "textural" | string }>;
  motifRotation: string[];
  texturePlan?: string[];
  assetFallbacks: string[];
  variationChecks: string[];
}

interface AssetUsePlan {
  defaultMode: "asset-rich" | "wireframe" | string;
  targetDistinctAssets: "5-10" | string;
  selectedAssets: Array<{
    id: string;
    source: "style-owned" | "shared-provider" | "user-provided" | "network" | "generated-bitmap" | "generated-vector" | string;
    pathOrUrl?: string;
    role: string;
    surfaces: string[];
    usage: "informational" | "identity" | "decorative" | "textural" | "iconic" | string;
  }>;
  checks: string[];
}

// AssetUseCheck is a delivery-time generation output, not a README/StyleLock field.
// The artifact build produces it and the quality gate must pass it before delivery.
interface AssetUseCheck {
  ok: boolean;                       // true only when no required fixes remain
  defaultMode: "asset-rich" | "wireframe" | string;
  distinctAssetCount: number;        // counted by the asset-count rules; routine shapes excluded
  targetRange: "5-10" | string;      // a guide range, not a hard quota
  countWithinTarget: boolean;        // false flags asset-thin or over-cluttered output; a restrained style may sit at the low end when semanticRelevance holds
  selectedAssets: AssetUsePlan["selectedAssets"];
  qualityFlags: {
    transparencyPreserved: boolean;  // RGBA kept; no unwanted opaque/white box around assets
    aspectRatioPreserved: boolean;   // no non-uniform stretching of informative assets
    readabilityPreserved: boolean;   // assets do not sit behind dense text or harm contrast
    semanticRelevance: boolean;      // each asset earns a role; no decorative filler
    rasterizationClean?: boolean;    // SVG->PNG/EMF conversions are crisp and transparent
  };
  issues: string[];
  requiredFixes: string[];
}
```

## Abstract Style Class

The style family is modeled as one abstract base class plus concrete implementation classes. The base workflow consumes only `DesignStyleBase`; every named style must be substitutable through the same methods.

```ts
abstract class DesignStyleBase {
  abstract resolve(request: DesignRequest): StyleResolution;
  abstract getIntent(): { intent: string; creativeLatitude: string[]; safetyBoundaries?: string[] };
  abstract getPalette(): {
    colorTokens: Record<string, { hex: string; role: string }>;
    seriesCards: SeriesColorCard[];
    sameFamilyProgressions: SameFamilyProgression[];
  };
  abstract getTypography(): TypographySystem;
  abstract getLayoutSystem(): LayoutRules;
  abstract getVisualRhythmSystem(medium: TargetMedium): VisualRhythmPlan;
  abstract getMediumTranslation(medium: TargetMedium): MediumRules;
  abstract getAssetPolicy(): AssetPolicy;
  abstract getSurfaceTexturePolicy(): SurfaceTexturePolicy;
  abstract getModifierCompatibility(): ModifierCompatibilityPolicy;
  abstract getPreviewOptions(request: DesignRequest, composedPlan: ComposedStylePlan): StylePreviewPlan;
  abstract applyStyleLock(styleLock: StyleLock, composedPlan: ComposedStylePlan): ComposedStylePlan;
  abstract selfCheck(outputDescription: string): CheckResult;
}

// Conceptual implementation classes; documentation uses `implements` to emphasize
// conformance to the base contract even when a target language would spell this
// relationship as inheritance.
class SeuDesignStyle implements DesignStyleBase {}
class RenminbiColorStyle implements DesignStyleBase {}
class ChineseTraditionalColorStyle implements DesignStyleBase {}
```

`resolve()` owns trigger matching and returns `StyleResolution`. The `get*()` methods expose design intent, palette, typography, layout, visual rhythm, medium translation, asset policy, surface texture policy, and modifier compatibility without forcing the base workflow to branch on a style name. `getModifierCompatibility()` is the style-specific contract for composing `StyleModifier[]` with the base style while preserving identity and safety boundaries. `selfCheck()` is the final style-specific quality gate.

## Required Provider Interfaces

A concrete style is valid only if its reference file supplies evidence for every `DesignStyleBase` method and for every provider interface below. These provider interfaces are the documented facets used by the abstract methods.

```ts
interface TriggerMatcher {
  names: string[];
  aliases: string[];
  domainCues: string[];
  defaultPolicy: string;
  match(request: DesignRequest): StyleResolution | null;
}

interface DesignIntentProvider {
  getIntent(): { intent: string; creativeLatitude: string[]; safetyBoundaries?: string[] };
}

interface PaletteProvider {
  getPalette(): {
    colorTokens: Record<string, { hex: string; role: string }>;
    seriesCards: SeriesColorCard[];
    sameFamilyProgressions: SameFamilyProgression[];
  };
}

interface TypographyProvider {
  getTypography(): {
    primaryFonts: string[];
    accentFonts?: string[];
    hierarchyRules: string[];
    fallbackRules: string[];
  };
}

interface LayoutSystem {
  getLayoutSystem(): {
    grid: string[];
    spacing: string[];
    density: string;
    hierarchy: string[];
    compositionRules: string[];
  };
}


interface VisualRhythmProvider {
  getVisualRhythmSystem(medium: TargetMedium): {
    rhythmScope: string;
    visualAnchorRule: string;
    archetypeVarietyRule: string;
    motifRotation: string[];
    assetFallbackRule: string;
    variationCheck: string[];
  };
}

interface ComponentTranslator {
  getMediumTranslation(medium: TargetMedium): MediumRules;
}

interface AssetPolicy {
  // Returned by DesignStyleBase.getAssetPolicy().
  assetRoot: `assets/${string}/`;
  importMode: "style-owned" | "user-provided-only" | "style-owned-visible" | "personal-visible-assets";
  manifestFile?: string;
  availableAssets: Record<string, AssetRole[]> | "none";
  placementRules: string[];
  distortionRules: string[];
  fallbackPolicy: string;
}

interface SurfaceTexturePolicy {
  // Returned by DesignStyleBase.getSurfaceTexturePolicy().
  provider: "none" | string;
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

interface ModifierCompatibilityProvider {
  // Returned by DesignStyleBase.getModifierCompatibility().
  acceptsModifiers: boolean;
  hardInvariants: string[];
  allowedTargets: Array<"palette" | "motif" | "texture" | "layout" | "mood" | "asset" | string>;
  allowedSources: Array<"style-owned" | "user-provided" | "generated-vector" | "shared-provider" | "code-native" | "none" | string>;
  defaultIntensity: "subtle" | "balanced" | "expressive";
  conflictPolicy: string;
  promotionPolicy: string;
  selfCheckRules: string[];
}

type ModifierCompatibilityPolicy = ModifierCompatibilityProvider;

interface PreviewNegotiationProvider {
  // Returned by DesignStyleBase.getPreviewOptions().
  getPreviewOptions(request: DesignRequest, composedPlan: ComposedStylePlan): StylePreviewPlan;
}

interface StyleLockApplier {
  // Returned by DesignStyleBase.applyStyleLock().
  applyStyleLock(styleLock: StyleLock, composedPlan: ComposedStylePlan): ComposedStylePlan;
}

interface QualityGate {
  selfCheck(outputDescription: string): CheckResult;
}
```

## Preview Negotiation Contract

Preview negotiation defaults to `previewMode: auto`. It is recommended for ambiguous, high-stakes, public-facing, brand-sensitive, or user-requested visual work, but it is not mandatory for ordinary direct artifact generation. For direct PPT, web, app, dashboard, or static visual requests, the model may create an internal `StyleLock` from defaults and proceed without user approval, then disclose important locked defaults in the final note.

Auto-mode sequence:

1. Build `ComposedStylePlan` from the base style and compatible modifiers.
2. Decide whether explicit preview is needed from user intent, ambiguity, stakes, and regeneration cost.
3. If preview is needed, call `getPreviewOptions(request, composedPlan)`, generate one preview image or preview surface from `StylePreviewPlan.previewPrompt`, present `StyleOptionSet[]`, and iterate until the user approves.
4. Build or confirm a `VisualRhythmPlan` and `AssetUsePlan` for multi-page/multi-screen work, including archetype sequence, visual anchors, motif rotation, selected visible assets, and sourced/generated materials.
5. If preview is not needed, choose default options from the active style's preview defaults and create an internal `StyleLock` that includes visual-rhythm decisions. For the palette/series default, do not lock a single habitual card: when the user named no palette and no decisive cue forces one, run `Default Series Selection` from `design_mechanics.md` to pick a context-fitting series with genuine variation, and disclose it as an auto-varied default.
6. Call `applyStyleLock(styleLock, composedPlan)` and generate the final artifact only from locked decisions.

Rules:

- `StyleOptionSet` values must come from the active style's palette, visual rhythm system, asset policy, visible asset boundary, surface texture policy, modifier compatibility rules, user-provided assets, generated assets, or network materials.
- Texture options may reference only tokens declared by the active style's `SurfaceTexturePolicy.allowedTokens`; include a texture-off option when turning texture off leaves a complete design.
- Palette options must preserve the active style's semantic color hierarchy and accessibility requirements.
- Final artifact generation stays aligned with locked palette, texture, layout density, visual rhythm, motif, or asset decisions. If a locked option cannot be implemented in the target medium, use an equivalent fallback already declared by the active style.
- A normal non-wireframe visual artifact should not lock `asset-off`, `motif-off`, or shape-only defaults globally. These options are local exceptions for dense pages or explicit wireframe requests.


## Visual Rhythm Contract

Visual rhythm is the deck/page-level planning layer that prevents a style from becoming either monotonous or arbitrarily decorative. It is mandatory for multi-slide decks, multi-screen flows, long pages, and dense static artifacts; for a single simple surface it may collapse to one anchor and one density rule.

For each generated artifact, the active style must provide or derive a `VisualRhythmPlan` before detailed composition:

1. Map each slide, screen, or major section to a declared archetype or explicit information role.
2. Assign at least one non-body-text visual anchor to each slide/screen/major section. Anchors may be informational, structural, decorative, or textural, but they must support hierarchy.
3. Rotate motif treatments, texture states, layout skeletons, and density levels to keep creative range visible across the artifact.
4. Use material discovery as a standard design-comparison input: compare runtime imagery with visible style-owned assets, shared texture providers, sourced candidates, generated bitmap/vector assets, user-provided assets, charts, diagrams, typographic labels, swatches, rules, and code-native geometry, then choose the style-faithful option with the strongest semantic and variation value.
5. For decks, websites, apps, dashboards, and static visuals, plan about 5-10 distinct assets or asset roles across the artifact. Count real files, generated assets, sourced images/icons, and texture providers; do not count ordinary rectangles, rules, text boxes, or basic chart shapes. When the visible inventory is thin, download or generate assets to reach that range.
6. Add variation checks to `selfCheckPlan` and final `Self-Check`; visual variety should preserve accessibility and style fidelity.

The visual rhythm plan is permission to explore scale, density, imagery, and motif range. When density or legibility calls for it, a slide can choose `motif-off` or `texture-off` while still keeping a clear content or structure anchor. It is not permission to make an entire artifact shape-only unless the user asks for a wireframe/data-diagram style.

## Modifier Composition Contract

Style modifiers are data-level overlays for user-requested changes that should not become new concrete styles by default. The base workflow may compose modifiers after style resolution, preserving base-style identity and assets while allowing expressive variants. Load `style_modifier_contract.md` when modifier extraction, compatibility checks, composition decisions, or modifier self-check rules are needed.

```ts
interface StyleComposer {
  compose(baseStyle: DesignStyleBase, modifiers: StyleModifier[]): ComposedStylePlan;
}
```

`ComposedStylePlan.reconciledChanges` should record any request that was softened, clarified, unavailable, or too strong for the base style. If a modifier would dominate the base style at `expressive` intensity, identify the result as a base-style variant or propose a new concrete style instead of presenting it as the untouched base style.

## Asset Provider Contract

Treat each style asset boundary as a runtime module rooted at `assets/<style_name>/`. The base workflow asks the active concrete style for abstract roles, handles, and fallback behavior, then inspects the visible files. Every concrete style must still provide the boundary directory and `ASSET_MANIFEST.md`; static validation checks that requirement without inspecting file inventories. An empty boundary means assets are downloaded or generated at runtime.

```ts
interface AssetProvider {
  styleName: StyleName;
  root: `assets/${string}/`;
  roles: AssetRole[];
  fallbackPolicy: string;
  resolve(role: AssetRole, medium: TargetMedium): RuntimeAssetHandle[];
}

interface RuntimeAssetHandle {
  handle: string;
  roles: AssetRole[];
  intrinsicRatio?: number;
  colorMode?: "color" | "mono" | "mixed" | "unknown";
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

interface SurfaceProvider {
  providerName: "transparent_textures" | string;
  fallbackPolicy: string;
  resolve(token: string, medium: TargetMedium): RuntimeSurfaceHandle | null;
}

interface RuntimeSurfaceHandle {
  token: string;
  visualCharacter: string;
  recommendedRoles: string[];
  defaultOpacity: [number, number];
  safePlacement: "tile" | "panel" | "edge-band" | string;
}
```

## Surface Texture Provider Source

When a style enables a shared texture provider, framework references may name the provider and abstract tokens, but provider records, source URLs, checksums, wrapper files, and index contents stay inside the opaque asset boundary or task-local documentation.

Enable a provider in a concrete style as a neutral tiled surface substrate with explicit fallback behavior. Provider availability should not imply a global ornament library or make framework validation depend on the provider's current files.

## Self-Check Output Contract

Concrete style `Self-Check` sections should produce or simulate this shape before delivery:

```ts
const result: CheckResult = {
  ok: boolean,              // true only when no required fixes remain
  issues: string[],         // concrete visual, contract, asset, or readability problems
  requiredFixes: string[],  // changes required before final delivery
};
```

Use style-specific checks inside that shape. For example, SEU checks logo aspect ratios and institutional fit; RMB checks denomination color logic and paper/ink layering; Chinese traditional color checks named-color and cultural-context fit. Multi-page or multi-screen outputs should also check visual anchor coverage, archetype variety, motif rotation, and whether any fallback asset strategy left pages visually empty.

For any non-wireframe visual artifact, delivery must also produce an `AssetUseCheck` alongside the `CheckResult`. The `AssetUseCheck` is a generation output (not a README or `StyleLock` field) that the quality gate inspects to confirm reasonable asset use: the distinct-asset count is in the 5-10 guide range (a guide, not a hard quota — a restrained style may sit at the low end when each asset earns a role; never pad to hit a number), available style-owned, provider, sourced, or generated assets were actually used instead of an all-code-native shortcut, vector assets that the medium cannot embed were rasterized to RGBA/PNG (or EMF) with transparency preserved, and every asset earns a semantic or structural role without harming aspect ratio, contrast, or readability. If `AssetUseCheck.ok` is false, resolve `requiredFixes` before delivery.

## Substitutability Rules

- The template workflow should not special-case one style after resolution; it should treat `SeuDesignStyle`, `RenminbiColorStyle`, and `ChineseTraditionalColorStyle` as `DesignStyleBase` instances.
- If one style needs a new behavior, first add a method or optional interface here, then let every style either implement it or explicitly declare `none`.
- If a user asks for palette, motif, texture, layout, mood, or asset adjustments, model them as `StyleModifier[]` and validate them through the selected style's `getModifierCompatibility()` policy unless they are permanent enough to justify a new concrete style.
- Every concrete style must document `Modifier Compatibility`; support may be permissive, restrictive, or `acceptsModifiers: false`, but it must be explicit so the abstract workflow remains substitutable.
- Every concrete style must expose preview options through `getPreviewOptions()` and honor approved or internally locked selections through `applyStyleLock()` so final outputs remain consistent with the `StyleLock`.
- Concrete styles may use style-owned, runtime-provided, network-sourced, or user-provided assets, but all must expose an `AssetPolicy` with a network/generation fallback and without requiring framework knowledge of current asset-folder contents.
- Concrete styles must also expose a `SurfaceTexturePolicy`, even if it declares `provider: none`. Surface providers are optional substrate services, not identity assets.
- A style may enable a non-`none` surface provider through stable policy handles, token lists, and fallback behavior; provider file verification belongs inside the runtime asset bundle.
- A style may be brand-led, color-led, or motif-led; the workflow should still consume it through the same methods.
- Medium translation must cover PPT, web, app/dashboard, and static visual output, even if the style simply says to reuse layout/color rules for a medium.
- Concrete styles must expose a `Visual Rhythm System`; multi-page and multi-screen outputs must use it to plan visual anchors, archetype variation, motif rotation, and variation checks before final generation.
