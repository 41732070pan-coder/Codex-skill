# seu_design_style

Use `seu_design_style` for designs inspired by the Southeast University master defense template and runtime SEU identity asset roles. It should feel academic, structured, calm, light, and institutional, with SEU green as structure and SEU yellow as measured emphasis.

## Contract Conformance

Implements `DesignStyleBase` as `SeuDesignStyle`.

Required runtime sections: Triggers, Intent, Creative Latitude, Color Tokens, Typography, Layout Principles, PPT Slide Archetypes, Visual Rhythm System, Web Translation, App / Dashboard Translation, Static Visual Translation, Asset Interface, Surface Texture Policy, Asset Rules, Modifier Compatibility, Preview Option Sets, Self-Check.

## Triggers

Use this style when the user asks for:

- `seu_design_style`, SEU style, Southeast University style, 东南大学, 东大, or UI Guide SEU template.
- Thesis defense, research presentation, academic report, lab/project showcase, school-branded deck, or institutional website/app.
- A PPT, web page, app UI, dashboard, or frontend demo that should follow the SEU template's design language.

## Intent

Design a reusable carrier for content, not a decorative poster. The page or screen should make titles, arguments, figures, tables, and workflows easy to replace. Brand elements should establish identity and page structure, while the content stays visually primary.

## Creative Latitude

- The style can range from research-dense to ceremonial-spacious as long as the page still feels academic, institutional, and reusable.
- Use SEU identity assets confidently on covers, transitions, headers, and closing pages; vary scale, placement, and motif intensity by information role.
- Explore architectural, botanical, motto, and rule-based motifs as structural devices, including richer cover treatments when the deck needs ceremony.
- Preserve identity asset aspect ratios and content legibility as safety boundaries for official marks and dense academic material.
- Keep main content in robust grids, columns, tables, or containers so expressive identity moments remain editable.

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

Use a light system by default: white or very light silver backgrounds, green for hierarchy, yellow for precise emphasis, plus white space, black text, silver rules, and occasional gold/orange accents to keep the palette alive.

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
| Section Transition | Chapter break | Large section number in yellow, green structural line, spacious title block, optional vertical architectural silhouette. |
| Title Text | Argument or explanation | Strong green title, subtitle, accent rule, readable body, optional right-side motto role or auxiliary architectural ornament. |
| Two Columns | Comparison or paired ideas | Symmetric columns, aligned starts, clear divider, small captions such as `Side A` and `Side B`. |
| Image Text | Figure plus interpretation | Image/diagram area and reading area; label them with small structural captions. |
| Process | Workflow or framework | Numbered steps, consistent boxes, yellow arrows or short bars, concise supporting text. |
| Chart Data | Results and takeaway | Figure area plus conclusion column; highlight key data with yellow, not large color fills. |
| Table Comparison | Metrics or methods | Use stable columns; emphasize the winning/own method with a yellow marker or subtle row treatment. |
| Closing / Q&A | Summary, thanks, contact | Reintroduce stronger identity assets such as motto, architectural, or botanical roles, but keep center message calm. |

For slide decks, use 16:9 by default.

## Visual Rhythm System

Use a deck-level visual rhythm plan so SEU identity feels deliberate instead of repeated or sparse.

- `rhythmScope`: for PPT decks, map each slide to an archetype before drawing; for web/app work, map each major view or section to an information role.
- `visualAnchorRule`: every slide or major screen needs one non-body-text anchor: approved SEU identity asset, architectural/botanical/motto motif, chart, table, process diagram, figure frame, numbered agenda block, or green/yellow rule system.
- `archetypeVarietyRule`: no more than two consecutive slides should use the same title/body skeleton; alternate identity-heavy moments, evidence/data pages, explanation pages, and transition pages.
- `motifRotation`: rotate logo lockup, architectural silhouette, motto role, botanical motif, thin green/yellow rules, and motif-off states; vary brand asset size and placement across pages.
- `assetFallbackRule`: when an SEU asset is not appropriate, use academic diagrams, aligned tables, figure labels, thin rules, and structured white space rather than decorative filler.
- `variationCheck`: confirm that white space, academic anchors, and brand motifs vary with the information role and keep the deck lively without crowding the message.

## Web Translation

For websites, build the actual useful page first: dashboard, research page, project detail, lab portal, event page, data interface, or a more expressive hero when the user's goal calls for it.

Use:

- A light header with thin green/yellow top rule.
- Compact logo lockup in the header; card-level identity can vary through rules, color, or small markers.
- Section titles with green text and the green/yellow accent rule.
- Dense but calm content areas for academic information, figures, tables, timelines, and evidence blocks.
- Cards only for repeated items or genuinely framed tools; keep border radius restrained, around 6-8px.
- Yellow for active nav, highlights, status dots, key metrics, or selected rows.
- Silver or soft green backgrounds for secondary panels.
- Footer or edge ornament using architectural auxiliary pattern at low opacity or small scale.

Use With Care:

- Rich hero treatments, shadows, and promotional card layouts can work when they still feel institutional and leave the actual information easy to scan.
- Full-screen brand blocks are strongest for admissions, ceremony, or keynote moments; research and dashboard pages should reveal useful content early.

## App / Dashboard Translation

Use an institutional operations feel:

- Left or top navigation with green active state and yellow accent marker.
- Tables, filters, tabs, segmented controls, and charts should be compact and scannable.
- Use chart palettes led by green, yellow, silver, black, and optional orange; reserve navy for contrast.
- Use badges and status indicators sparingly. Prefer icons plus concise labels.
- Keep repeated components aligned to a stable grid so dynamic data does not resize cards or shift controls unexpectedly.

## Static Visual Translation

For posters, title cards, diagrams, thumbnails, or static presentation visuals:

- Lead with a light field, strong SEU green structure, and one measured yellow accent.
- Use official identity assets only as anchors: top-left header, side rail, cover block, or closing mark.
- Keep decorative architectural or botanical motifs low-density and outside the main reading path.
- Prefer diagram clarity, aligned captions, and stable figure labels over poster-like decoration.
- Preserve all logo, wordmark, motto, and motif aspect ratios exactly.

## Asset Interface

Use only SEU asset roles exposed by the runtime `AssetPolicy`. The asset boundary is opaque and may be edited by users; this style file does not enumerate or verify its files.

- `assetRoot`: `assets/seu_design_style/`.
- `importMode`: `style-owned`.
- `manifestFile`: opaque asset-bundle provenance handle.
- `availableAssets`: official identity marks, wordmarks, lockups, motto artwork, architectural motifs, color-card roles, and botanical motif roles when exposed by the runtime policy.
- `usageRoles`: identity mark, header lockup, cover anchor, side rail, footer band, section transition anchor, low-opacity background motif, and closing accent.
- `placementRules`: use contain-style placement for identity assets; use repetition or cropping only for explicitly decorative architectural patterns.
- `fallbackPolicy`: if an asset cannot be inspected or placed without distortion, use SEU green/yellow rules, typography, and layout structure rather than forcing the asset into the composition.

## Surface Texture Policy

SEU texture support is enabled through the `transparent_textures` provider handle, but only as a low-opacity neutral paper substrate behind institutional color, grid, and approved SEU identity roles.

- `provider`: `transparent_textures`
- `assetRoot`: `assets/transparent_textures/`
- `manifestFile`: `opaque transparent_textures manifest handle`
- `indexFile`: `opaque transparent_textures index handle`
- `provenanceFile`: `opaque transparent_textures provenance handle`
- `defaultToken`: `textured-paper`
- `allowedTokens`: ["textured-paper", "clean-gray-paper"]
- `opacityRange`: [0.02, 0.06]
- `allowedSurfaces`: ["slide-background", "section-divider", "quiet-panel", "web-section"]
- `protectedSurfaces`: ["dense paragraph text", "small table cells", "official logo area", "motto artwork area", "architectural/botanical motif overlap"]
- `fallbackPolicy`: disable texture and keep the SEU feel through green/yellow rules, silver panels, grid structure, and approved runtime asset roles.

Use texture only when it stays below content and does not compete with SEU identity marks.

## Asset Rules

Aspect ratio is a hard requirement:

- Read each runtime asset's intrinsic ratio from available metadata before placement.
- Fit identity marks, wordmarks, motto artwork, architectural silhouettes, and botanical motifs into the intended region with contain-style sizing. Center them or align them to a meaningful edge, but do not stretch them to match both the placeholder width and height.
- For PPT generation, compute the displayed `w` and `h` from the intrinsic ratio and the maximum allowed box. Treat the box as a boundary, not as the final forced dimensions.
- For web/app work, set `height: auto` or `width: auto`, use `object-fit: contain` for informative assets, and reserve `object-fit: cover` only for intentionally cropped photographic or background areas.
- Decorative architectural patterns may be clipped or repeated as background texture when needed, but they should still not be non-uniformly scaled. If a pattern cannot fill a region without distortion, crop it, repeat it, or use a simpler rule instead.
- When the exact intrinsic size cannot be read, use a square or measured conservative placeholder only until the asset is inspected visually; do not guess a forced aspect ratio for official identity marks.

Runtime asset handles:

- Use only abstract asset roles exported by the active policy, such as identity, wordmark, lockup, motto, architectural motif, pattern, color-card, or botanical motif roles.
- Name abstract roles rather than fixed files from this style reference; file-level details belong inside the asset boundary.
- Use monochrome or lower-emphasis variants only when the runtime policy exposes them and color would compete with content. Keep aspect ratios intact; a slightly smaller correctly proportioned asset is always preferable to a larger distorted one.

## Modifier Compatibility

Use modifiers only as controlled overlays on the SEU base style. The standard style remains light, academic, structured, content-first, and led by SEU green with SEU yellow as precise accent.

- `acceptsModifiers`: true.
- `allowedTargets`: palette, motif, texture, layout, mood, asset.
- `allowedSources`: style-owned, user-provided, generated-vector, code-native, shared-provider only when explicitly enabled by the surface policy, and none.
- `defaultIntensity`: subtle for content pages, balanced for cover or section transitions.
- `conflictPolicy`: compose modifiers around SEU identity hierarchy, light academic structure, official asset boundaries, and content-first layout; clarify requests that would replace the SEU identity system.
- `promotionPolicy`: promote recurring expressive variants such as an autumn-crimson SEU deck into a new concrete style only when they need durable palette rules, assets, registry metadata, or validators.

Core identity anchors:

- SEU green remains the primary structure and hierarchy color for titles, headers, rules, section systems, and navigation states.
- SEU yellow works best as a precise accent for short rules, active markers, and key highlights.
- The artifact stays reusable and content-first even when covers or transitions become more ceremonial.
- Official SEU identity asset roles from the runtime policy remain distinct from modifier motifs, user-provided decoration, or generated graphics.
- Modifier motifs are described as seasonal or decorative unless they are added to the SEU runtime asset policy through a separate style update.
- Main content stays in robust grids, columns, tables, or containers.

Allowed soft modifiers:

- Seasonal or event-specific accent palettes, when added as secondary accents rather than replacements for SEU green/yellow.
- Low-opacity code-native or generated-vector botanical motifs, when clearly decorative and outside the main reading path.
- User-provided decorative motifs, when provenance is acceptable and placement respects identity and readability.
- Layout-density adjustments that preserve the stable academic grid.

SEU-compatible autumn example:

| Modifier | Tokens / Motifs | Strong Use | Use With Care |
| --- | --- | --- | --- |
| Deep crimson accent | `#7A1E2C`, `#9D2933`, `#B36D61`, `#F3E6E3` | Secondary seasonal accent, quote-rule edge, section-page detail, small footer line, abstract maple motif color. | Global title, header, navigation, or primary structure color when the output should remain standard SEU style. |
| Maple motif | Abstract vector or user-provided decorative motif | Cover corner, section transition, footer strip, low-opacity edge ornament. | Official identity mark, logo substitute, dense content background, or repeated high-intensity system motif. |

For balanced autumn variants, use SEU green for structure, SEU yellow for precise highlights, deep crimson for secondary atmosphere, and maple motifs only as decorative modifiers. If the user asks for crimson or maple to dominate the deck, label the result as an expressive SEU-inspired variant or propose a new concrete style instead of presenting it as standard `seu_design_style`.

## Preview Option Sets

`getPreviewOptions(request, composedPlan)` exposes preview choices. In `previewMode: auto`, explicit preview is used only when ambiguity, stakes, brand sensitivity, or user request requires it. Otherwise the model creates an internal `StyleLock` from the default option sets and proceeds. When a preview is used, it should show a title/header sample, SEU green/yellow palette strip, a content card, a quiet panel, an approved SEU identity or motif placement, and the active texture substrate. `applyStyleLock(styleLock, composedPlan)` preserves the locked texture, layout density, palette hierarchy, and asset placement decisions in the final artifact.

| Option Set | Target | Default | Options | Rules |
| --- | --- | --- | --- | --- |
| `seu-texture` | texture | `textured-paper` | `textured-paper`; `clean-gray-paper`; `texture-off` | Tokens come from `allowedTokens`; keep opacity in `[0.02, 0.06]`; protect logos, motto artwork, dense text, table cells, and SEU motif overlaps. |
| `seu-layout-density` | layout | `academic-balanced` | `academic-balanced`; `research-dense`; `ceremonial-spacious` | Keep stable grids and content-first hierarchy even when the deck or page becomes more poster-like. |
| `seu-identity-emphasis` | asset | `header-lockup` | `header-lockup`; `cover-anchor`; `quiet-footer-mark`; `motif-off` | Use only runtime assets exposed by this style policy; preserve intrinsic aspect ratios; decorative motifs stay secondary. |

Preview option behavior:

- `textured-paper` gives the default soft institutional paper grain.
- `clean-gray-paper` gives a cooler, more restrained substrate for dashboards, data pages, and research-heavy sections.
- `texture-off` disables provider texture while retaining SEU style through green/yellow structure, silver panels, typography, grids, and approved runtime assets.
- Style locks record the selected texture token or `texture-off`, selected density, selected identity emphasis, and any softened modifiers.

## Self-Check

Return or simulate this `CheckResult` before finishing:

- `ok`: true only when no required fixes remain.
- `issues`: list any concrete SEU style, layout, asset, readability, or responsive problems.
- `requiredFixes`: list required revisions before delivery.

Minimum checks:

- The artifact is reusable and content-first.
- The background is mostly light.
- Green carries hierarchy; yellow is only an accent.
- Identity and motif assets are sharp and not distorted; their displayed width/height matches the intrinsic aspect ratio when metadata is available.
- Main content uses robust grids/columns/tables rather than fragile absolute placement.
- Text fits on mobile and desktop, or inside slide placeholders.
- Brand elements appear with purpose and do not crowd the message.
- Tables, charts, and key/value rows align cleanly.
- Multi-slide or multi-screen work has visual anchors on every surface, no long run of repeated layout skeletons, and a documented motif/asset fallback when brand assets are not used.
- For web/app work, inspect responsive views and make sure no UI text overlaps.
- No unavailable shared texture provider is referenced in the output.
