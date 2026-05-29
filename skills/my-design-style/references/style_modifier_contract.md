# Style Modifier Contract

Use this contract when a user asks for a named base style plus extra preferences such as a new accent color, seasonal motif, texture, denser layout, softer mood, or user-provided decorative asset. A modifier is a controlled overlay on a base style, not a new concrete style by default.

## When To Use Modifiers

Use `StyleModifier[]` when:

- The base style is still clear and should remain dominant.
- The requested change is local, seasonal, tonal, or one-off.
- The change can be accepted, downgraded, or rejected without creating a new style reference file.
- The requested asset is user-provided, generated as simple code-native/vector decoration, or comes from a declared provider.

Create or propose a new concrete style instead when:

- The modifier becomes the main identity system.
- The request needs a durable palette, asset package, layout family, and self-check.
- The base style invariants would no longer pass.
- Multiple future tasks should reuse the same variant as a named style.

## Data Shapes

```ts
type ModifierTarget = "palette" | "motif" | "texture" | "layout" | "mood" | "asset";
type ModifierOperation = "add" | "replace" | "increase" | "decrease" | "tint";
type ModifierPriority = "hard" | "soft";
type ModifierIntensity = "subtle" | "balanced" | "expressive";
type ModifierSource =
  | "style-owned"
  | "user-provided"
  | "generated-vector"
  | "shared-provider"
  | "code-native"
  | "none";

interface StyleModifier {
  id: string;
  target: ModifierTarget;
  operation: ModifierOperation;
  priority: ModifierPriority;
  intensity?: ModifierIntensity;
  source?: ModifierSource;
  value: string | Record<string, unknown>;
  compatibilityRules: string[];
  selfCheckRules?: string[];
}

interface ComposedStylePlan {
  baseStyle: StyleName;
  modifiers: StyleModifier[];
  acceptedChanges: string[];
  rejectedOrDowngradedChanges: string[];
  palettePlan?: Record<string, unknown>;
  motifPlan?: Record<string, unknown>;
  assetPlan?: Record<string, unknown>;
  selfCheckPlan: string[];
}

interface StyleComposer {
  compose(baseStyle: DesignStyleBase, modifiers: StyleModifier[]): ComposedStylePlan;
}
```

## Composition Workflow

1. Resolve the base style first.
2. Extract requested modifiers from explicit wording, source assets, `brandRequirements`, and constraints.
3. Read base-style invariants from intent, anti-goals, palette, asset policy, surface policy, and self-check.
4. Classify each modifier by target, operation, priority, intensity, source, and role.
5. Accept compatible modifiers, downgrade over-strong modifiers, and reject unsafe or unavailable modifiers.
6. Produce a `ComposedStylePlan` before generating the artifact.
7. Run the base style self-check plus all modifier self-check rules.

## Conflict Handling

- Hard base-style invariants outrank soft modifiers.
- A soft modifier may add an accent, motif, or mood only if the base style remains recognizable.
- A `replace` operation must be treated as risky. Do not replace identity colors, official marks, or required layout structure unless the user explicitly chooses a new style direction.
- `expressive` modifiers should be labeled as a variant of the base style. If they repeatedly recur, propose a new concrete style.
- Record every downgrade or rejection in `ComposedStylePlan.rejectedOrDowngradedChanges`.

## Asset Source Rules

- `style-owned`: only assets declared by the active style's `AssetPolicy` and manifest.
- `user-provided`: use only for the current request unless the user asks to install or register the asset.
- `generated-vector` or `code-native`: use simple abstract geometry or vector motifs; do not imitate official marks, seals, protected logos, currency, or copyrighted scans.
- `shared-provider`: allowed only when the provider has files, manifest, provenance, and the active style permits it.
- `none`: use color, layout, typography, and simple rules instead of external assets.

Modifier assets are not official base-style assets unless the active style manifest declares them. Decorative motifs must not replace logo, wordmark, motto, institutional marks, or required identity anchors.

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
- Modifier intensity matches the user's request and the final visual weight.
- Downgraded or rejected modifier requests are disclosed when they affect the output.

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
        "Must not replace SEU logo, wordmark, motto, auditorium, or pine assets.",
        "Must stay outside the main reading path.",
        "Must be abstract/vector-like, not photographic filler."
      ],
      selfCheckRules: [
        "Maple motif is decorative and never described as official SEU identity.",
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
        "Deep crimson must not replace global title/header green.",
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
  rejectedOrDowngradedChanges: [
    "Do not make crimson the global title, header, or structure color.",
    "Do not treat maple motifs as SEU official assets."
  ],
  palettePlan: {
    hierarchy: "SEU green",
    preciseAccent: "SEU yellow",
    seasonalAccent: "deep crimson / maple red",
    wash: "red-wash only on high-contrast surfaces"
  },
  motifPlan: {
    officialIdentity: "SEU assets from active style manifest",
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
