# Style Modifier Contract

Use this contract when a user asks for a named base style plus extra preferences such as a new accent color, seasonal motif, texture, denser layout, softer mood, or user-provided decorative asset. A modifier is a controlled overlay on a base style, not a new concrete style by default.

## When To Use Modifiers

Use `StyleModifier[]` when:

- The base style is still clear and should remain dominant.
- The requested change is local, seasonal, tonal, or one-off.
- The change can be composed, softened, or clarified without creating a new style reference file.
- The requested asset is visible in the active style boundary, user-provided, generated, sourced from a no-login/no-paywall external material source, or comes from a declared provider.

Create or propose a new concrete style instead when:

- The modifier becomes the main identity system.
- The request needs a durable palette, asset package, layout family, and self-check.
- The base style invariants would no longer pass.
- Multiple future tasks should reuse the same variant as a named style.

## Data Shapes

Canonical data shapes for `StyleModifier`, `ComposedStylePlan`, and related style composition records live in `references/style_contract.md`. This file only defines modifier extraction, compatibility checks, conflict handling, and examples.

## Composition Workflow

1. Resolve the base style first.
2. Extract requested modifiers from explicit wording, source assets, `brandRequirements`, and constraints.
3. Read base-style invariants and modifier rules from `DesignStyleBase.getModifierCompatibility()`, plus intent, creative latitude, palette, asset policy, surface policy, and self-check.
4. Classify each modifier by target, operation, priority, intensity, source, and role.
5. Accept compatible modifiers, soften over-strong modifiers when needed, and clarify only concrete blockers: public/commercial rights, impersonation, sensitive identity use, legal-tender/security-document reproduction, inaccessible contrast, missing files, or unavailable network access.
6. Produce a `ComposedStylePlan` before generating the artifact.
7. Run the base style self-check plus all modifier self-check rules.

## Conflict Handling

- Hard base-style invariants from `getModifierCompatibility()` outrank soft modifiers.
- A soft modifier may add an accent, motif, or mood only if the base style remains recognizable.
- Treat a `replace` operation as a possible style-direction change; preserve identity colors, official marks, or required layout structure unless the user explicitly chooses a new direction.
- `expressive` modifiers should be labeled as a variant of the base style. If they repeatedly recur, propose a new concrete style.
- Record every softened, clarified, or refused change in `ComposedStylePlan.reconciledChanges`.

## Asset Source Rules

- `style-owned`: only assets exposed by the active style's runtime `AssetPolicy`.
- `user-provided`: use only for the current request unless the user asks to install or register the asset.
- `generated-vector` or `generated-bitmap`: use original generated material when the style needs richer imagery or when official marks, seals, protected logos, currency, or copyrighted scans would raise concrete public/commercial risk.
- `network`: use no-login/no-paywall task-local materials when the user has not forbidden browsing and the material improves semantic fit or visual variety; keep source notes and apply stricter review only for public/commercial/sensitive outputs.
- `code-native`: use original geometry for structure, diagrams, charts, and simple ornament; do not use code-native shapes as a global replacement for available assets.
- `shared-provider`: allowed when the active style exposes a provider handle, fallback behavior, and provenance expectations.
- `none`: use only for local asset-off exceptions, wireframes, dense data surfaces, explicit user constraints, or concrete safety blockers. Record the reason if an entire artifact uses this source.

Modifier assets become official base-style assets only when the active style policy exposes them at runtime. Decorative motifs should complement logo, wordmark, motto, institutional marks, or required identity anchors. For personal/internal work, visible assets do not need commercial-grade clearance before use, but the final note or task QA should identify the asset source/path and role.

## Intensity Levels

| Intensity | Meaning | Typical Limits |
| --- | --- | --- |
| `subtle` | Small local accent. | Corners, footers, low-opacity marks, tiny color chips, no layout shift. |
| `balanced` | Noticeable but secondary. | Cover/section pages may show the modifier; content pages remain base-style led. |
| `expressive` | Strong mood or seasonal variant. | Label as a base-style variant; preserve invariants or propose a new concrete style. |

## Self-Check Additions

Modifier self-checks should verify:

- The base style still passes its own self-check.
- Added colors meet contrast needs and do not replace protected identity roles.
- Added motifs stay outside the main reading path unless the base style permits stronger placement.
- Asset provenance and allowed source are clear.
- A normal non-wireframe artifact uses enough visual assets or asset roles for richness; fewer than 5 requires a recorded exception.
- Modifier intensity matches the user's request and the final visual weight.
- Softened, clarified, or refused modifier requests are disclosed when they affect the output.

## Example: SEU With Maple And Deep Crimson

```ts
const plan: ComposedStylePlan = {
  baseStyle: "seu_design_style",
  modifiers: [
    {
      id: "maple_motif",
      target: "motif",
      operation: "add",
      priority: "soft",
      intensity: "balanced",
      source: "generated-vector",
      value: {
        motif: "abstract maple leaf",
        role: "decorative",
        placement: ["cover-corner", "section-transition", "footer-strip"],
        opacity: "low-to-medium"
      },
      compatibilityRules: [
        "Keep SEU identity, wordmark, motto, architectural, and botanical asset roles intact.",
        "Must stay outside the main reading path.",
        "Use an abstract/vector-like treatment with clear visual purpose."
      ],
      selfCheckRules: [
        "Maple motif is decorative and described separately from official SEU identity.",
        "Motif does not crowd titles, figures, tables, or speaker metadata."
      ]
    },
    {
      id: "deep_crimson_accent",
      target: "palette",
      operation: "add",
      priority: "soft",
      intensity: "balanced",
      source: "none",
      value: {
        "deep-crimson": "#7A1E2C",
        "maple-red": "#9D2933",
        "muted-red": "#B36D61",
        "red-wash": "#F3E6E3"
      },
      compatibilityRules: [
        "SEU green remains the structural hierarchy color.",
        "Deep crimson remains a secondary accent beside global title/header green.",
        "Red wash may be used only when text contrast remains strong."
      ],
      selfCheckRules: [
        "Crimson appears as secondary seasonal accent only.",
        "SEU green and light academic structure remain dominant."
      ]
    }
  ],
  acceptedChanges: [
    "Use abstract maple motifs as decorative secondary elements.",
    "Add deep crimson as a seasonal accent palette."
  ],
  reconciledChanges: [
    "Crimson was kept secondary rather than made the global title, header, or structure color.",
    "Maple motifs were treated as decorative seasonal assets rather than SEU official assets."
  ],
  palettePlan: {
    hierarchy: "SEU green",
    preciseAccent: "SEU yellow",
    seasonalAccent: "deep crimson / maple red",
    wash: "red-wash only on high-contrast surfaces"
  },
  motifPlan: {
    officialIdentity: "SEU identity asset roles exposed by the active style policy",
    seasonalDecoration: "abstract generated maple vectors"
  },
  assetPlan: {
    officialAssets: "style-owned SEU assets only",
    modifierAssets: "generated vector decoration, not official identity"
  },
  selfCheckPlan: [
    "Run SEU self-check.",
    "Verify maple and crimson remain secondary modifiers."
  ]
};
```
