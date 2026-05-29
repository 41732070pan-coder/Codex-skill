# Style Registry

This registry is the concrete-style lookup table for `my-design-style`. Use it to resolve style names, aliases, domain cues, priorities, and stable asset-policy handles. Detailed behavior belongs in each concrete style file; asset-folder contents remain opaque runtime data.

## Registry Entries

| Style | Reference | Aliases | Domain cues | Medium cues | Priority | Asset root | Use when |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `seu_design_style` | `references/seu_design_style.md` | SEU; Southeast University; 东南大学; campus academic | academic; institutional; university; thesis defense; research report; campus brand | ppt; web; app; dashboard; document_visual; static_visual; design_template | domain-default | `assets/seu_design_style/` | The artifact should feel like an SEU institutional, academic, research, or campus-branded design. |
| `renminbi_color_style` | `references/renminbi_color_style.md` | RMB; yuan; renminbi; Chinese banknote; 人民币; 纸币风格 | finance; commerce; fintech; auction; collection; value; settlement; trustworthy financial culture | ppt; web; app; dashboard; document_visual; static_visual; design_template | domain-default | `none` | The artifact should borrow legal, non-counterfeit visual cues from RMB color, paper, numerals, and fine-line financial texture while using runtime assets only through the active policy. |
| `chinese_traditional_color_style` | `references/chinese_traditional_color_style.md` | traditional Chinese colors; guofeng; 国风; 中式传统色; classical Chinese | museum; cultural; editorial; heritage; Chinese palette; classical brand; literary or historical context | ppt; web; app; dashboard; document_visual; static_visual; design_template | domain-default | `none` | The artifact should use named Chinese traditional colors and restrained cultural composition while using runtime assets only through the active policy and avoiding generic ornament. |

## Entry Shape

```ts
interface StyleRegistryEntry {
  styleName: string;
  referenceFile: `references/${string}.md`;
  aliases: string[];
  domainCues: string[];
  mediumCues: TargetMedium[];
  priority: "explicit-only" | "domain-default" | "fallback-never";
  assetRoot: `assets/${string}/` | "none";
  useWhen: string;
}
```

## Resolution Rules

- Exact `Style` name wins.
- Exact alias match wins over domain cues.
- Strong domain cue plus compatible `Medium cues` may select a `domain-default` style when the user did not name a style.
- `explicit-only` styles can be selected only by name or alias.
- `fallback-never` styles are never selected implicitly.
- If two styles match with similar confidence, ask once instead of blending them.
- Do not mix concrete style files unless the user explicitly requests a hybrid; a hybrid still needs one primary style and one secondary influence.
- Never use assets from a style that is not the active concrete implementation.

## Adding A New Style

1. Create `references/<style_name>.md` from `references/style_template.md`.
2. Add one row to `Registry Entries` with all structured fields populated.
3. Declare only a stable `assetRoot` handle and fallback behavior. Do not document whether the corresponding asset boundary is empty or populated, and keep file names, provenance rows, and checksums inside the asset bundle or task documentation.
4. Run `python skills/my-design-style/scripts/validate_styles.py`.

## Contract Conformance Requirement

Every concrete style file must contain a concise `Contract Conformance` section near the top. The section should name its `DesignStyleBase` implementation and list the required runtime sections instead of repeating the full interface/provider map. Detailed interface definitions belong in `references/style_contract.md`; static validation checks section presence, visual rhythm metadata, asset-policy handles, surface-provider metadata shape, and fallback fields without inspecting `assets/`.

Required runtime sections: Triggers, Intent, Anti-Goals, Color Tokens, Typography, Layout Principles, PPT Slide Archetypes, Visual Rhythm System, Web Translation, App / Dashboard Translation, Static Visual Translation, Asset Interface, Surface Texture Policy, Asset Rules, Modifier Compatibility, Preview Option Sets, Self-Check.

Asset availability is a runtime concern. A style must define `AssetPolicy` handles and fallback behavior, but framework documents must not assert whether a style currently has bundled files or enumerate those files.
