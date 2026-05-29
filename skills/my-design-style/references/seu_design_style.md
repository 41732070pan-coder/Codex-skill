# seu_design_style

Use `seu_design_style` for designs inspired by the Southeast University master defense template and bundled SEU identity assets. It should feel academic, structured, calm, light, and institutional, with SEU green as structure and SEU yellow as measured emphasis.

## Implementation Map

Implementation class: `SeuDesignStyle implements DesignStyleBase`. The table below maps the abstract base methods and their provider facets to concrete document sections.

| Interface / Method | Implemented by |
| --- | --- |
| `DesignStyleBase.resolve(request)` | `Triggers` |
| `DesignStyleBase.getIntent()` | `Intent`, `Anti-Goals` |
| `DesignStyleBase.getPalette()` | `Color Tokens`, `Series Color Cards`, `Same-Family Progression Cards` |
| `DesignStyleBase.getTypography()` | `Typography` |
| `DesignStyleBase.getLayoutSystem()` | `Layout Principles` |
| `DesignStyleBase.getMediumTranslation(medium)` | `PPT Slide Archetypes`, `Web Translation`, `App / Dashboard Translation`, `Static Visual Translation` |
| `DesignStyleBase.getAssetPolicy()` | `Asset Interface`, `Asset Rules` |
| `DesignStyleBase.getSurfaceTexturePolicy()` | `Surface Texture Policy` |
| `DesignStyleBase.selfCheck(output)` | `Self-Check` |
| `TriggerMatcher` | `Triggers` |
| `DesignIntentProvider` | `Intent`, `Anti-Goals` |
| `PaletteProvider` | `Color Tokens`, `Series Color Cards`, `Same-Family Progression Cards` |
| `TypographyProvider` | `Typography` |
| `LayoutSystem` | `Layout Principles` |
| `ComponentTranslator` | `PPT Slide Archetypes`, `Web Translation`, `App / Dashboard Translation`, `Static Visual Translation` |
| `AssetPolicy` | `Asset Interface`, `Asset Rules` |
| `SurfaceTexturePolicy` | `Surface Texture Policy` |
| `QualityGate` | `Self-Check` |

## Triggers

Use this style when the user asks for:

- `seu_design_style`, SEU style, Southeast University style, 东南大学, 东大, or UI Guide SEU template.
- Thesis defense, research presentation, academic report, lab/project showcase, school-branded deck, or institutional website/app.
- A PPT, web page, app UI, dashboard, or frontend demo that should follow the SEU template's design language.

## Intent

Design a reusable carrier for content, not a decorative poster. The page or screen should make titles, arguments, figures, tables, and workflows easy to replace. Brand elements should establish identity and page structure, while the content stays visually primary.

## Anti-Goals

- Keep the default visual system light rather than relying on full-page dark backgrounds.
- Prefer SVG or vector identity assets when they are available.
- Avoid overloading one page with logo, wordmark, motto, auditorium, pine, and multiple patterns at high intensity.
- Use decoration only when it supports identity, hierarchy, or structure.
- Preserve the aspect ratio of logos, school marks, motto, and auditorium motifs.
- Keep main content in robust grids, columns, tables, or containers instead of fragile absolute placement.

## Color Tokens

| Token | Hex | Role |
| --- | --- | --- |
| `seu-green` | `#587558` | Primary identity, titles, headers, structure lines, section numbers, navigation states. |
| `seu-yellow` | `#FDD000` | Primary accent, short rules, data highlights, section markers, active indicators. |
| `seu-black` | `#231815` | Body text, table text, strong UI labels. |
| `assist-orange` | `#F6AB00` | Secondary emphasis and optional chart highlight. |
| `assist-navy` | `#151E49` | Deep contrast only for small blocks or special cases, not default page backgrounds. |
| `seu-gold` | `#AD986E` | Quiet separators, weak emphasis, refined decorative lines. |
| `seu-silver` | `#B4B7B9` | Light backgrounds, table rules, support panels. |
| `white` | `#FFFFFF` | Main background. |

Use a light system: white or very light silver backgrounds, green for hierarchy, yellow for precise emphasis. Avoid one-note green screens; balance with white space, black text, silver rules, and occasional gold/orange accents.

### Series Color Cards

Every design using this style must start from one of these series cards. If the target artifact does not need a specific SEU identity emphasis, use the default `SEU Light Institutional` card.

| Series | Primary | Auxiliary Colors | Neutral / Base | Use |
| --- | --- | --- | --- | --- |
| SEU Light Institutional | `#587558` | `#FDD000`, `#AD986E`, `#F6AB00` | `#FFFFFF`, `#F5F6F3`, `#231815`, `#B4B7B9` | Default decks, websites, app screens, research reports. |
| SEU Green Structure | `#587558` | `#6F8B6C`, `#8DA38A`, `#DCE5D8` | `#FFFFFF`, `#EEF0EC`, `#231815`, `#B4B7B9` | Dense academic UI, navigation, section systems, tables. |
| SEU Yellow Highlight | `#FDD000` | `#F6AB00`, `#AD986E`, `#587558` | `#FFFFFF`, `#F8F4DF`, `#231815`, `#B4B7B9` | Active states, key findings, agenda numbers, chart highlights. |
| Default Neutral Fallback | `#231815` | `#FFFFFF`, `#B4B7B9`, `#EEF0EC` | `#FFFFFF`, `#F5F5F5`, `#231815`, `#6B6B6B` | Use only when no brand color should lead. |

### Same-Family Progression Cards

SEU identity should still use same-family progression instead of repeating the same green or yellow in every emphasis slot.

| Family | Primary | Support-Strong | Support-Mid | Support-Soft | Wash | Muted-Bridge |
| --- | --- | --- | --- | --- | --- | --- |
| SEU Green | `#587558` | `#3F5F43` | `#6F8B6C` | `#8DA38A` | `#DCE5D8` | `#B4B7B9` |
| SEU Yellow | `#FDD000` | `#F6AB00` | `#AD986E` | `#F8E58B` | `#F8F4DF` | `#B4B7B9` |

Suggested UI token mapping:

```css
:root {
  --seu-green: #587558;
  --seu-yellow: #fdd000;
  --seu-black: #231815;
  --seu-orange: #f6ab00;
  --seu-navy: #151e49;
  --seu-gold: #ad986e;
  --seu-silver: #b4b7b9;
  --surface: #ffffff;
  --surface-soft: #f5f6f3;
  --surface-muted: #eef0ec;
  --text: #231815;
  --text-mid: rgba(35, 24, 21, 0.70);
  --text-weak: rgba(35, 24, 21, 0.58);
}
```

## Typography

- Prefer clean sans-serif typography.
- For Chinese: Source Han Sans SC, Noto Sans CJK SC, Microsoft YaHei, or SimHei fallback.
- For Latin: Arial or a neutral sans-serif fallback.
- Keep headings strong but not oversized. Academic content needs room for charts, tables, and explanations.
- Use small English captions in restrained all-caps or small caps for secondary entry labels such as `Evidence`, `Reading`, `Figure`, `Takeaway`, `Method / Metric Comparison`.

## Layout Principles

- Use relative, content-safe layout structures: grids, columns, flex, tabular layouts, minipages, CSS grid, container queries.
- Reserve absolute positioning for background motifs, fixed headers/footers, or subtle identity ornaments.
- Maintain clear columns and stable alignment for key/value metadata, agenda numbers, table columns, cards, and process steps.
- Treat white space as intentional breathing room. Empty space should not look like a missing image, failed ornament, or undersized content block.
- Use thin green rules plus short yellow rules as a recurring identity gesture.
- Use decorative motifs at low intensity in headers, footers, side rails, or section transitions.

## PPT Slide Archetypes

Design around these reusable slide/page types:

| Archetype | Purpose | Style notes |
| --- | --- | --- |
| Cover | Title, author, advisor, college, date | Strong identity zone; vertical or stacked logo is acceptable; keep metadata aligned in stable rows. |
| Agenda | 3-5 sections | Numbered list with fixed columns; logo mark or side identity column may appear once. |
| Section Transition | Chapter break | Large section number in yellow, green structural line, spacious title block, optional vertical auditorium silhouette. |
| Title Text | Argument or explanation | Strong green title, subtitle, accent rule, readable body, optional right-side motto or auxiliary auditorium ornament. |
| Two Columns | Comparison or paired ideas | Symmetric columns, aligned starts, clear divider, small captions such as `Side A` and `Side B`. |
| Image Text | Figure plus interpretation | Image/diagram area and reading area; label them with small structural captions. |
| Process | Workflow or framework | Numbered steps, consistent boxes, yellow arrows or short bars, concise supporting text. |
| Chart Data | Results and takeaway | Figure area plus conclusion column; highlight key data with yellow, not large color fills. |
| Table Comparison | Metrics or methods | Use stable columns; emphasize the winning/own method with a yellow marker or subtle row treatment. |
| Closing / Q&A | Summary, thanks, contact | Reintroduce stronger identity assets such as motto, auditorium, or pine, but keep center message calm. |

For slide decks, use 16:9 by default.

## Web Translation

For websites, avoid turning this into a marketing hero unless the user explicitly asks for one. Build the actual useful page first: dashboard, research page, project detail, lab portal, event page, or data interface.

Use:

- A light header with thin green/yellow top rule.
- Compact logo lockup in the header; never repeat it in every card.
- Section titles with green text and the green/yellow accent rule.
- Dense but calm content areas for academic information, figures, tables, timelines, and evidence blocks.
- Cards only for repeated items or genuinely framed tools; keep border radius restrained, around 6-8px.
- Yellow for active nav, highlights, status dots, key metrics, or selected rows.
- Silver or soft green backgrounds for secondary panels.
- Footer or edge ornament using auditorium auxiliary pattern at low opacity or small scale.

Avoid:

- Purple/blue gradient hero treatments.
- Decorative blobs, heavy shadows, and large rounded promotional cards.
- Big full-screen brand blocks that obscure actual information.

## App / Dashboard Translation

Use an institutional operations feel:

- Left or top navigation with green active state and yellow accent marker.
- Tables, filters, tabs, segmented controls, and charts should be compact and scannable.
- Use chart palettes led by green, yellow, silver, black, and optional orange; reserve navy for contrast.
- Use badges and status indicators sparingly. Prefer icons plus concise labels.
- Keep repeated components aligned to a stable grid. Dynamic data must not resize cards or shift controls unexpectedly.

## Static Visual Translation

For posters, title cards, diagrams, thumbnails, or static presentation visuals:

- Lead with a light field, strong SEU green structure, and one measured yellow accent.
- Use official identity assets only as anchors: top-left header, side rail, cover block, or closing mark.
- Keep decorative auditorium or pine motifs low-density and outside the main reading path.
- Prefer diagram clarity, aligned captions, and stable figure labels over poster-like decoration.
- Preserve all logo, wordmark, motto, and motif aspect ratios exactly.

## Asset Interface

Bundled assets are in `assets/seu_design_style/`. Use SVG files directly for web/app and convert to vector formats for PPT/PDF workflows when needed.

- `assetRoot`: `assets/seu_design_style/`.
- `importMode`: `style-owned`.
- `manifestFile`: `assets/seu_design_style/ASSET_MANIFEST.md`.
- `availableAssets`: official logo marks, wordmarks, logo lockups, motto artwork, auditorium motifs, color card, and pine motif listed in `ASSET_MANIFEST.md` and summarized below.
- `usageRoles`: identity mark, header lockup, cover anchor, side rail, footer band, section transition anchor, low-opacity background motif, and closing accent.
- `placementRules`: use contain-style placement for identity assets; use repetition or cropping only for explicitly decorative auditorium patterns.
- `fallbackPolicy`: if an asset cannot be inspected or placed without distortion, use SEU green/yellow rules, typography, and layout structure rather than forcing the asset into the composition.

## Surface Texture Policy

No shared surface texture provider is currently bundled for this skill, so SEU texture support is disabled by default.

- `provider`: `none`.
- `assetRoot`: `none`.
- `manifestFile`: `none`.
- `defaultToken`: none.
- `allowedTokens`: none.
- `opacityRange`: 0-0% until a real provider is added.
- `allowedSurfaces`: none.
- `forbiddenSurfaces`: dense paragraph text, small table cells, official logo area, motto artwork area, auditorium/pine motif overlap.
- `fallbackPolicy`: keep the SEU feel through green/yellow rules, silver panels, grid structure, and approved SEU SVG assets.

Future texture support may be added only after a provider directory, manifest, index, provenance, and validator support exist.

## Asset Rules

Aspect ratio is a hard requirement:

- Read each asset's intrinsic ratio from its SVG `viewBox`, `width`/`height`, or raster metadata before placement.
- Fit logos, wordmarks, motto artwork, auditorium silhouettes, and pine motifs into the intended region with contain-style sizing. Center them or align them to a meaningful edge, but do not stretch them to match both the placeholder width and height.
- For PPT generation, compute the displayed `w` and `h` from the intrinsic ratio and the maximum allowed box. Treat the box as a boundary, not as the final forced dimensions.
- For web/app work, set `height: auto` or `width: auto`, use `object-fit: contain` for informative assets, and reserve `object-fit: cover` only for intentionally cropped photographic or background areas.
- Decorative auditorium patterns may be clipped or repeated as background texture when needed, but they should still not be non-uniformly scaled. If a pattern cannot fill a region without distortion, crop it, repeat it, or use a simpler rule instead.
- When the exact intrinsic size cannot be read, use a square or measured conservative placeholder only until the asset is inspected visually; do not guess a forced aspect ratio for official identity marks.

Key assets:

| Asset | Use |
| --- | --- |
| `01_logo_mark_color.svg` | Compact mark, agenda side rail, app icon-like identity. |
| `06_logo_combo_cn_en_horizontal_color.svg` | General page/header identity. |
| `16_logo_combo_cn_en_vertical_color.svg` | Cover or tall identity block. |
| `19_motto_horizontal.svg` | Closing or formal identity moment. |
| `20_motto_vertical.svg` | Side rail or content-page ornament. |
| `21_auditorium_single.svg` | Closing/header decorative band. |
| `22_auditorium_pattern.svg` | Cover/agenda identity texture. |
| `23_auditorium_aux_single.svg` | Right-side or corner ornament. |
| `24_auditorium_aux_pattern.svg` | Footer/header weak decorative strip. |
| `26_auditorium_silhouette_vertical.svg` | Section transition anchor. |
| `27_pine.svg` | Closing or cultural identity accent. |

Use monochrome variants when color would compete with content. Keep aspect ratios intact; a slightly smaller correctly proportioned asset is always preferable to a larger distorted one.

## Self-Check

Return or simulate this `CheckResult` before finishing:

- `ok`: true only when no required fixes remain.
- `issues`: list any concrete SEU style, layout, asset, readability, or responsive problems.
- `requiredFixes`: list required revisions before delivery.

Minimum checks:

- The artifact is reusable and content-first.
- The background is mostly light.
- Green carries hierarchy; yellow is only an accent.
- Logos and motifs are vector, sharp, and not distorted; their displayed width/height matches the intrinsic aspect ratio.
- Main content uses robust grids/columns/tables rather than fragile absolute placement.
- Text fits on mobile and desktop, or inside slide placeholders.
- Brand elements appear with purpose and do not crowd the message.
- Tables, charts, and key/value rows align cleanly.
- For web/app work, inspect responsive views and make sure no UI text overlaps.
- No unavailable shared texture provider is referenced in the output.
