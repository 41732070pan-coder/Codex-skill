# renminbi_color_style

Use `renminbi_color_style` for designs inspired by the color language of Chinese RMB banknotes. It should feel valuable, layered, civic, tactile, and quietly premium, with banknote color families translated into modern PPT, web, app, dashboard, and editorial interfaces.

This is a color-and-layout style, not a currency reproduction kit. Use interpreted color, linework, watermark-like depth, and denomination logic. Do not recreate legal tender, portraits, serial numbers, official seals, anti-counterfeit marks, or full banknote layouts.

## Contract Conformance

Implements `DesignStyleBase` as `RenminbiColorStyle`.

Required runtime sections: Triggers, Intent, Anti-Goals, Color Tokens, Typography, Layout Principles, PPT Slide Archetypes, Visual Rhythm System, Web Translation, App / Dashboard Translation, Static Visual Translation, Asset Interface, Surface Texture Policy, Asset Rules, Modifier Compatibility, Preview Option Sets, Self-Check.

## Triggers

Use this style when the user asks for:

- `renminbi_color_style`, RMB style, yuan style, CNY style, Chinese banknote style, Chinese money color style.
- 人民币色彩, 人民币配色, 纸币配色, 钞票配色, 钱币配色, 国潮金融, 中式金融视觉, or Chinese banknote-inspired visuals.
- Finance, payment, wealth management, accounting, commerce, fintech, marketplace, auction, collection, business report, annual review, or premium Chinese cultural branding.
- PPT decks, websites, app screens, dashboards, posters, or design assets that should feel refined and culturally Chinese without becoming a literal red-and-gold festival theme.

## Source Reading

The practical source palette comes from the fifth-series RMB denomination families:

- 100 yuan: red.
- 50 yuan: green.
- 20 yuan: brown / warm ochre.
- 10 yuan: blue / blue-black.
- 5 yuan: purple.
- 1 yuan: olive green.

Use those families as role colors. Fashion and color-composition references also suggest useful pairings: blue with gray for calmness, purple with white, brown, or small black accents for control, and earth colors with similar saturation for harmony.

## Intent

Create a trustworthy, content-first design that borrows the sophistication of banknote printing: layered color, fine rules, measured contrast, dense but orderly information, and soft paper-like surfaces. The result should feel like value, credibility, and cultural memory, not a literal pile of cash.

## Anti-Goals

- Do not reproduce actual RMB banknote fronts or backs, portraits, denomination numerals, serial numbers, seals, official emblems, security threads, watermarks, or anti-counterfeit details.
- Do not use realistic banknote scans as UI backgrounds unless the user explicitly provides lawful editorial assets and the use is clearly documentary.
- Avoid "rich = red + gold everywhere." Gold is a thread or glint, not the whole page.
- Avoid casino, luxury-club, gambling, or aggressive sales aesthetics.
- Avoid muddy vintage filters that make text low contrast.
- Avoid one-note red pages. Even when 100-yuan red leads, balance it with paper, ink, gray, ochre, green, or blue.
- Do not use decorative linework so densely that charts, tables, and UI controls become hard to read.

## Color Tokens

These color tokens are taken from the provided RMB palette cards. Treat each denomination as a complete series: the darkest or most characteristic color is usually the primary, while the remaining colors are auxiliary colors for tints, charts, panels, gradients, and decorative linework.

| Token | Hex | Role |
| --- | --- | --- |
| `rmb-100-primary` | `#BD0E2B` | 100-yuan red primary value color, headlines, important metrics, confident brand moments. |
| `rmb-100-light` | `#F6ACB9` | 100-yuan pale pink auxiliary, soft panels, backgrounds, chart tint. |
| `rmb-100-soft` | `#D4606D` | 100-yuan muted red auxiliary, secondary marks and chart series. |
| `rmb-100-bright` | `#E94136` | 100-yuan bright red auxiliary, urgent deltas or active emphasis. |
| `rmb-100-deep` | `#C93649` | 100-yuan deep rose auxiliary, selected states and section accents. |
| `rmb-50-primary` | `#496B61` | 50-yuan green primary, trust, banking, compliance, stable dashboard navigation. |
| `rmb-50-lavender` | `#CEC7D9` | 50-yuan cool lavender auxiliary, quiet contrast and secondary panels. |
| `rmb-50-bluegray` | `#7C81A4` | 50-yuan blue-gray auxiliary, data and neutral series. |
| `rmb-50-mint` | `#99BFB2` | 50-yuan mint auxiliary, positive backgrounds and soft cards. |
| `rmb-50-teal` | `#527A72` | 50-yuan teal auxiliary, structure lines and active states. |
| `rmb-20-primary` | `#6A4D31` | 20-yuan brown primary, commerce, revenue, auction, grounded storytelling. |
| `rmb-20-cream` | `#F2C98B` | 20-yuan warm cream auxiliary, paper-like panels and soft highlights. |
| `rmb-20-tan` | `#E0AB81` | 20-yuan tan auxiliary, category fills and chart series. |
| `rmb-20-taupe` | `#93786A` | 20-yuan taupe auxiliary, secondary text blocks and subtle rules. |
| `rmb-20-dark` | `#462D25` | 20-yuan dark brown auxiliary, high contrast and formal anchors. |
| `rmb-10-primary` | `#364A88` | 10-yuan blue primary, analysis, ledger, data products, calm B2B UI. |
| `rmb-10-pale` | `#CFE3ED` | 10-yuan pale blue auxiliary, cool backgrounds and cards. |
| `rmb-10-cyan` | `#97D6F3` | 10-yuan cyan auxiliary, charts, links, and technical highlights. |
| `rmb-10-steel` | `#8AA2C4` | 10-yuan steel blue auxiliary, secondary series and table emphasis. |
| `rmb-10-slate` | `#5872A5` | 10-yuan slate blue auxiliary, navigation states and section structure. |
| `rmb-5-primary` | `#443459` | 5-yuan purple primary, premium, collection, membership, cultural editorial surfaces. |
| `rmb-5-sage` | `#CECFB0` | 5-yuan sage auxiliary, soft backgrounds and contrast panels. |
| `rmb-5-beige` | `#D8C8B3` | 5-yuan beige auxiliary, paper surfaces and warm balance. |
| `rmb-5-mauve` | `#A18DB0` | 5-yuan mauve auxiliary, secondary accents and charts. |
| `rmb-5-violet` | `#77608E` | 5-yuan violet auxiliary, active states and refined markers. |
| `rmb-1-primary` | `#363E25` | 1-yuan olive primary, natural balance, low-intensity finance, support panels. |
| `rmb-1-gray` | `#B6B4A7` | 1-yuan gray auxiliary, neutral surfaces and quiet chart series. |
| `rmb-1-khaki` | `#CCBB84` | 1-yuan khaki auxiliary, warm highlights and category accents. |
| `rmb-1-pale` | `#BFC9AD` | 1-yuan pale green auxiliary, success backgrounds and soft panels. |
| `rmb-1-olive` | `#747E61` | 1-yuan olive auxiliary, structure lines and selected states. |
| `rmb-gold-thread` | `#C8A968` | Thin rules, icons, small dividers, special badges, not large fills. |
| `rmb-paper` | `#F6F0E4` | Main warm paper background. |
| `rmb-paper-cool` | `#EEF2EC` | Cool pale background for green or blue pages. |
| `rmb-watermark` | `#E3D8C4` | Low-contrast watermark blocks, subtle panels, inactive surfaces. |
| `rmb-ink` | `#241A17` | Main body text. |
| `rmb-gray` | `#6D716C` | Secondary text, captions, axes, metadata. |
| `white` | `#FFFFFF` | Clean content surface and high-contrast relief. |

### Series Color Cards

Every design using this style must start from at least one series card. Each card has a primary color and matching auxiliary colors; combine it with the neutral / base colors shown in the same row. If the task has no clear denomination or color direction, use `Default Neutral Fallback`.

| Series | Primary | Auxiliary Colors | Neutral / Base | Use |
| --- | --- | --- | --- | --- |
| 100 Yuan Red | `#BD0E2B` | `#F6ACB9`, `#D4606D`, `#E94136`, `#C93649` | `#FFFFFF`, `#F6F0E4`, `#241A17`, `#6D716C` | Primary value, annual report, important metrics, confident brand moments. |
| 50 Yuan Green | `#496B61` | `#CEC7D9`, `#7C81A4`, `#99BFB2`, `#527A72` | `#FFFFFF`, `#EEF2EC`, `#241A17`, `#6D716C` | Trust, banking, compliance, portfolio health, stable dashboards. |
| 20 Yuan Ochre | `#6A4D31` | `#F2C98B`, `#E0AB81`, `#93786A`, `#462D25` | `#FFFFFF`, `#F6F0E4`, `#241A17`, `#6D716C` | Commerce, revenue, auction, inventory, trade storytelling. |
| 10 Yuan Blue | `#364A88` | `#CFE3ED`, `#97D6F3`, `#8AA2C4`, `#5872A5` | `#FFFFFF`, `#EEF2EC`, `#241A17`, `#D9DEE5` | Analysis, ledger, data product, account overview, calm B2B UI. |
| 5 Yuan Purple | `#443459` | `#CECFB0`, `#D8C8B3`, `#A18DB0`, `#77608E` | `#FFFFFF`, `#F6F0E4`, `#6D716C`, `#E3D8C4` | Premium, collection, membership, cultural editorial surfaces. |
| 1 Yuan Olive | `#363E25` | `#B6B4A7`, `#CCBB84`, `#BFC9AD`, `#747E61` | `#FFFFFF`, `#EEF2EC`, `#241A17`, `#6D716C` | Low-intensity finance, support panels, success states, natural balance. |
| Default Neutral Fallback | `#241A17` | `#FFFFFF`, `#6D716C`, `#E3D8C4`, `#F6F0E4` | `#FFFFFF`, `#F5F5F5`, `#241A17`, `#6D716C` | Use only when no denomination family should lead. |

### Same-Family Progression Cards

RMB cards are the model for the shared same-family progression rule: one denomination hue supplies a primary and several related supports. Use them to create emphasis, secondary marks, and smooth transitions without repeating the primary everywhere.

| Family | Primary | Support-Strong | Support-Mid | Support-Soft | Wash | Muted-Bridge |
| --- | --- | --- | --- | --- | --- | --- |
| 100 Yuan Red | `#BD0E2B` | `#C93649` | `#D4606D` | `#F6ACB9` | `#FBDEE4` | `#B96A73` |
| 50 Yuan Green | `#496B61` | `#527A72` | `#99BFB2` | `#CEC7D9` | `#EEF2EC` | `#7C81A4` |
| 20 Yuan Ochre | `#6A4D31` | `#462D25` | `#93786A` | `#E0AB81` | `#F2C98B` | `#A88462` |
| 10 Yuan Blue | `#364A88` | `#5872A5` | `#8AA2C4` | `#97D6F3` | `#CFE3ED` | `#6D716C` |
| 5 Yuan Purple | `#443459` | `#77608E` | `#A18DB0` | `#D8C8B3` | `#CECFB0` | `#6D716C` |
| 1 Yuan Olive | `#363E25` | `#747E61` | `#BFC9AD` | `#CCBB84` | `#EEF2EC` | `#B6B4A7` |

Suggested UI token mapping:

```css
:root {
  --rmb-100-primary: #bd0e2b;
  --rmb-100-light: #f6acb9;
  --rmb-100-soft: #d4606d;
  --rmb-100-bright: #e94136;
  --rmb-100-deep: #c93649;
  --rmb-50-primary: #496b61;
  --rmb-50-lavender: #cec7d9;
  --rmb-50-bluegray: #7c81a4;
  --rmb-50-mint: #99bfb2;
  --rmb-50-teal: #527a72;
  --rmb-20-primary: #6a4d31;
  --rmb-20-cream: #f2c98b;
  --rmb-20-tan: #e0ab81;
  --rmb-20-taupe: #93786a;
  --rmb-20-dark: #462d25;
  --rmb-10-primary: #364a88;
  --rmb-10-pale: #cfe3ed;
  --rmb-10-cyan: #97d6f3;
  --rmb-10-steel: #8aa2c4;
  --rmb-10-slate: #5872a5;
  --rmb-5-primary: #443459;
  --rmb-5-sage: #cecfb0;
  --rmb-5-beige: #d8c8b3;
  --rmb-5-mauve: #a18db0;
  --rmb-5-violet: #77608e;
  --rmb-1-primary: #363e25;
  --rmb-1-gray: #b6b4a7;
  --rmb-1-khaki: #ccbb84;
  --rmb-1-pale: #bfc9ad;
  --rmb-1-olive: #747e61;
  --rmb-gold-thread: #c8a968;
  --rmb-paper: #f6f0e4;
  --rmb-paper-cool: #eef2ec;
  --rmb-watermark: #e3d8c4;
  --rmb-ink: #241a17;
  --rmb-gray: #6d716c;
  --surface: #ffffff;
  --surface-soft: #fbf7ef;
  --border-subtle: rgba(36, 26, 23, 0.14);
  --text: #241a17;
  --text-mid: rgba(36, 26, 23, 0.72);
  --text-weak: rgba(36, 26, 23, 0.54);
}
```

## Palette Recipes

Use one denomination family as the lead, then add paper, ink, and one restrained secondary family.

| Recipe | Palette | Use |
| --- | --- | --- |
| 100 Yuan Report | `rmb-100-primary`, `rmb-100-light`, `rmb-paper`, `rmb-ink`, `rmb-gold-thread` | Annual summary, value proposition, primary finance storytelling. |
| 50 Yuan Trust | `rmb-50-primary`, `rmb-50-mint`, `rmb-50-bluegray`, `rmb-paper-cool`, `rmb-ink` | Banking, compliance, portfolio health, operations dashboard. |
| 20 Yuan Commerce | `rmb-20-primary`, `rmb-20-cream`, `rmb-20-tan`, `rmb-paper`, `rmb-gray` | Marketplace, revenue, inventory, auction, trade. |
| 10 Yuan Analysis | `rmb-10-primary`, `rmb-10-pale`, `rmb-10-cyan`, `rmb-paper-cool`, `rmb-gray` | Analytics, ledgers, data products, calm B2B UI. |
| 5 Yuan Premium | `rmb-5-primary`, `rmb-5-sage`, `rmb-5-beige`, `rmb-5-mauve`, `rmb-ink` | Membership, collection, premium benefits, editorial moments. |
| Denomination Set | Red, green, ochre, blue, purple, olive | Multi-series charts and category systems; keep saturation and lightness balanced. |

For charts, choose colors from the full denomination cards: blue, green, ochre, purple, red-soft, and olive before using pure red. Reserve `rmb-100-primary` for totals, risks, or the primary series.

## Typography

- Prefer modern, highly legible Chinese sans-serif typography: Source Han Sans SC, Noto Sans CJK SC, Microsoft YaHei, PingFang SC, or HarmonyOS Sans.
- For a formal or editorial accent, a Song/Ming face can be used for large titles only: Source Han Serif SC, Noto Serif CJK SC, or SimSun fallback.
- Use tabular numerals for money, percentages, account IDs, and dashboard metrics.
- Keep body text dark ink on paper or white surfaces. Avoid brown-on-paper for dense paragraphs.
- Use compact labels for financial UI: `Revenue`, `Cash Flow`, `Holdings`, `Risk`, `Settlement`, `Invoice`, `Market`.
- Do not over-letterspace Chinese. Use weight, size, and spacing for hierarchy instead.

## Layout Principles

- Use a tokenized spacing system based on 4px / 8px increments. For dense interfaces, use 8, 12, 16, 24, 32, 48, 64. For presentation sections, use 24, 32, 48, 64, 96.
- Build pages on a clear grid. For web and dashboards, use 12 columns or a responsive CSS grid. For PPT, use stable left/right or title/content regions.
- Use fine engraved-line gestures: thin rules, parallel separators, border insets, corner ticks, and light guilloche-inspired curves. Keep them low opacity and outside reading paths.
- Use watermark-like panels behind section markers or empty areas, not behind dense body text.
- Make money and numbers easy to compare: align decimals, keep units consistent, use fixed-width metric cells, and avoid wrapping key financial values.
- Use restrained radii: 4-8px for cards, tables, filters, and inputs.
- Use shadows lightly. Prefer border, inset line, and surface layering over heavy elevation.
- Keep decorative density highest on covers, section transitions, and hero/editorial surfaces; keep dashboards and tables quiet.

## PPT Slide Archetypes

Design around these reusable slide/page types:

| Archetype | Purpose | Style notes |
| --- | --- | --- |
| Cover | Title, organization, date, report scope | Lead with one denomination palette; use large calm title, paper field, thin gold-thread rule, and subtle linework. |
| Executive Summary | 3-5 key figures | Metric tiles with tabular numerals; red or green only for priority signals. |
| Denomination Agenda | Sections or chapters | Map sections to color families: red, green, ochre, blue, purple, olive. |
| Section Transition | Chapter break | Large color field or watermark block; sparse text; fine-line border or corner ticks. |
| Financial Statement | Income, expense, balance, cash flow | Dense table, strong alignment, minimal fills, subtle row grouping. |
| Chart Data | Trends and comparisons | Paper/white chart area; denomination set for series; red reserved for key result. |
| Risk / Compliance | Controls, exposure, audit status | Blue-black and green lead; use badges and status lines instead of loud warning blocks. |
| Commerce / Marketplace | Product, auction, order, or invoice flow | Ochre and red-soft accents; process rows and item cards. |
| Collection / Culture | Currency, auction, heritage, museum, object story | Purple or ochre lead; larger imagery; caption-rich layout. |
| Closing / Q&A | Thanks, contact, next steps | Return to paper, ink, gold-thread line, and one confident color accent. |

For slide decks, use 16:9 by default.

## Visual Rhythm System

Use a deck-level visual rhythm plan so the RMB-inspired language feels valuable and layered without becoming a repeated paper template or currency copy.

- `rhythmScope`: for PPT decks, assign every slide to a financial, report, data, culture, or transition archetype; for web/app work, assign each section to a product, metric, table, or editorial role.
- `visualAnchorRule`: every slide or major section needs one non-body-text anchor: metric tile group, denomination color strip, chart, statement table, abstract fine-line block, corner tick, process row, product/object image, or controlled paper texture.
- `archetypeVarietyRule`: alternate high-value title pages, dense financial tables, chart evidence, risk/compliance panels, and summary moments; do not repeat the same metric-card grid for long runs.
- `motifRotation`: rotate fine rules, corner ticks, abstract guilloche-inspired curves, denomination strips, texture-off states, and table/charts; linework must stay original and never imitate security features.
- `assetFallbackRule`: if no lawful imagery is available, use data visualization, tabular numerals, denomination swatches, paper/ink contrast, bundled abstract SVG assets, and original vector geometry rather than red-gold filler.
- `antiMonotonyCheck`: verify that each page has a value/data/culture anchor, red and gold do not dominate by repetition, and visual variety never increases counterfeit risk.

## Web Translation

For websites, build the useful experience first: fintech landing section, account overview, auction catalog, pricing page, transaction dashboard, report portal, or editorial story.

Use:

- Warm paper or cool paper page backgrounds with white content surfaces.
- A compact header with ink text, a thin denomination-colored rule, and one active color.
- Hero sections with real product, data, or cultural imagery when relevant. Do not rely on abstract red-gold gradients.
- Section titles paired with a short fine rule or corner tick.
- Tables with clear row height, fixed numeric alignment, and soft separators.
- Cards only for repeated objects or framed tools. Keep cards flat, bordered, and compact.
- Icon buttons and concise controls for finance workflows; avoid decorative pill overload.

Avoid:

- Full-screen red backgrounds unless the deliverable is explicitly celebratory.
- Faux banknotes as backgrounds.
- Dense guilloche textures behind text.
- Gold text on red for important body copy.

## App / Dashboard Translation

Use a trustworthy financial-operations feel:

- Navigation can be blue-black, green, or paper with a colored active bar.
- Metrics should use tabular numerals, stable widths, and concise labels.
- Filters, date ranges, tabs, segmented controls, and export buttons should be visible and compact.
- Positive, neutral, and risk states should not rely only on red/green. Pair color with text, icon, or shape.
- Use red sparingly for primary value, risk, or urgent deltas. Use green for confirmed/healthy states, blue for analysis, ochre for pending/commercial, purple for premium/special.
- Keep data visualization palettes balanced by saturation. Do not mix neon UI colors with paper-like banknote colors.
- Validate responsive behavior carefully. Currency values, CNY symbols, and long Chinese labels must not overlap.

## Static Visual Translation

For posters, title cards, diagrams, thumbnails, or static financial visuals:

- Choose one denomination family as the lead and build hierarchy through its progression card.
- Use paper/ink surfaces, fine rules, corner ticks, and original linework instead of banknote scans.
- Keep numbers, units, and labels aligned and readable; do not let decoration sit behind dense text.
- Use red and gold as signals, not full-page decoration unless the user explicitly asks for a celebratory visual.
- Avoid anything that resembles printable legal tender.

## Asset Interface

This style exposes a small style-owned SVG asset module for safe, non-currency financial ornament.

- `assetRoot`: `assets/renminbi_color_style/`.
- `importMode`: `manifested-svg`.
- `manifestFile`: `assets/renminbi_color_style/ASSET_MANIFEST.md`.
- `availableAssets`: `denomination_value_strip`, `financial_corner_frame`, `abstract_fine_line_wave`, `watermark_panel`.
- `usageRoles`: denomination color strips, report corner frames, low-opacity original fine-line depth, watermark-like card panels, generated in-artifact linework, original icons, and lawful user-provided imagery.
- `placementRules`: preserve aspect ratio; keep decorative linework outside reading paths and away from data labels; never imitate a printable banknote; use at most one major financial ornament per slide or screen.
- `fallbackPolicy`: use denomination color progressions, financial layout rhythm, tables, chart systems, coded fine rules, and the bundled manifest assets before considering any external personal-use asset.

For RMB-inspired work:

- Do not copy legal tender, seals, serial textures, official banknote artwork, portraits, denomination numerals, or anti-counterfeit marks.
- Build value through color progression, fine rules, tables, chart systems, secure-feeling layout rhythm, and the style-owned abstract assets.
- `01_denomination_value_strip.svg` is for hierarchy and palette rhythm, not denomination reproduction.
- `02_financial_corner_frame.svg` and `04_watermark_panel.svg` can structure covers, report summaries, and dashboard hero cards, but should not become a full voucher/banknote frame.
- `03_abstract_fine_line_wave.svg` may be used at low opacity as original linework; never combine it into security-pattern zones.
- Prefer modern financial UI structure over decorative currency imitation.

## Surface Texture Policy

RMB-inspired texture support is enabled through the bundled `transparent_textures` provider, but only as abstract paper tactility. It must never mimic security paper, anti-counterfeit marks, serial zones, official seals, or legal-tender surfaces.

- `provider`: `transparent_textures`
- `assetRoot`: `assets/transparent_textures/`
- `manifestFile`: `assets/transparent_textures/TEXTURE_MANIFEST.md`
- `indexFile`: `assets/transparent_textures/texture_index.json`
- `provenanceFile`: `assets/transparent_textures/provenance.md`
- `defaultToken`: `paper-fibers`
- `allowedTokens`: ["paper-fibers", "textured-paper", "clean-gray-paper"]
- `opacityRange`: [0.02, 0.05]
- `allowedSurfaces`: ["broad-background", "card-panel", "edge-band", "cover-wash"]
- `forbiddenSurfaces`: ["dense text", "chart labels", "serial-like marks", "seal-like marks", "legal-tender imitation zones", "anti-counterfeit-like artwork"]
- `fallbackPolicy`: disable texture and keep the style through denomination color progressions, paper/ink contrast, fine rules, financial grids, tables, and original code-native geometry.

Texture must remain a generic tactile substrate and must not resemble real banknote security features.

## Asset Rules

Bundled assets are available under `assets/renminbi_color_style/` and must be selected through `ASSET_MANIFEST.md`. Prefer these original SVG assets, generated vectors, or coded ornaments over copied banknote imagery.

Allowed:

- Manifested style-owned assets: `01_denomination_value_strip.svg`, `02_financial_corner_frame.svg`, `03_abstract_fine_line_wave.svg`, and `04_watermark_panel.svg`.
- Abstract fine-line patterns inspired by engraving or guilloche, created from simple curves, repeated rules, or low-opacity CSS/SVG.
- Watermark-like circles, floral silhouettes, landscape contours, or architectural outlines when they are original or sourced lawfully.
- Paper grain, fiber speckles, and subtle print misregistration only when they do not reduce legibility.
- Original iconography for wallet, invoice, ledger, chart, settlement, vault, auction, collection, and exchange.

Avoid:

- Actual RMB scans, cropped Mao portraits, Great Hall / Potala / Guilin / Three Gorges / Taishan / West Lake reproductions lifted from banknotes.
- Real-looking denominations, serial numbers, seals, watermarks, security lines, or anti-counterfeit marks.
- Any layout that could be confused with a printable banknote.

## Modifier Compatibility

RMB modifiers are supported only when they preserve the banknote-inspired abstraction and non-counterfeit safety boundary. Use modifiers as controlled overlays after selecting the RMB base style, not as a way to reproduce legal tender.

- `acceptsModifiers`: true.
- `allowedTargets`: palette, motif, texture, layout, mood, asset.
- `allowedSources`: style-owned when declared, user-provided, generated-vector, code-native, shared-provider only when explicitly enabled by the surface policy, and none.
- `defaultIntensity`: subtle for product/UI work, balanced for editorial or PPT section moments.
- `conflictPolicy`: preserve non-counterfeit anti-goals, readability, and denomination-family logic; downgrade or reject modifiers that imitate banknotes, official seals, serial numbers, anti-counterfeit details, portraits, or legal tender layouts.
- `promotionPolicy`: promote recurring named variants such as a durable fintech-blue mode, premium-auction mode, or compliance-dashboard mode into a concrete style only when they need their own palette, layout rules, registry metadata, or validation.

Hard invariants:

- Never recreate actual RMB banknote fronts/backs, portraits, serial numbers, official emblems, seals, security threads, watermark details, or complete denomination layouts.
- Preserve the selected denomination or palette recipe as the primary color logic; added colors should be secondary accents unless the user explicitly chooses a different registered style.
- Keep typography, rules, and linework content-first; decorative micro-linework must not reduce chart, table, or UI legibility.
- Do not use modifier assets as currency reproductions or imply official financial authorization.

Allowed soft modifiers:

- Additional accent colors that bridge from the selected denomination family into product, dashboard, or editorial needs.
- Abstract generated-vector linework, guilloche-inspired curves, watermark-like depth, or paper-like surfaces that do not copy real currency security features.
- Layout-density adjustments for reports or dashboards when information hierarchy remains orderly.
- User-provided documentary assets only when their use is lawful, clearly contextual, and not used as decorative UI background.

Modifier self-check additions:

- The output still reads as banknote-inspired design, not currency reproduction.
- Added motifs are abstract and do not copy protected RMB details.
- Added colors support the chosen denomination or documented palette recipe.
- Any rejected or downgraded currency-like request is disclosed.

## Preview Option Sets

`getPreviewOptions(request, composedPlan)` exposes preview choices. In `previewMode: auto`, explicit preview is used only when ambiguity, stakes, brand sensitivity, legal-tender sensitivity, or user request requires it. Otherwise the model creates an internal `StyleLock` from the default option sets and proceeds. When a preview is used, it should show the selected denomination palette, paper/ink contrast, abstract fine-line components, a metric card, a table or chart fragment, and any texture choice. It must demonstrate RMB-inspired abstraction without copying legal tender. `applyStyleLock(styleLock, composedPlan)` must preserve the locked denomination family, texture, linework strength, and non-counterfeit boundaries in the final artifact.

| Option Set | Target | Default | Options | Rules |
| --- | --- | --- | --- | --- |
| `rmb-palette-series` | palette | context-dependent, often `100-yuan-red` for value/report emphasis | `100-yuan-red`; `50-yuan-green`; `20-yuan-ochre`; `10-yuan-blue`; `5-yuan-purple`; `1-yuan-olive`; `neutral-fallback` | Use a complete series card; preserve auxiliary colors and paper/ink neutrals; do not reduce the style to red-and-gold decoration. |
| `rmb-paper-texture` | texture | `paper-fibers` | `paper-fibers`; `textured-paper`; `clean-gray-paper`; `texture-off` | Tokens must come from `allowedTokens`; keep opacity in `[0.02, 0.05]`; never imitate security paper, serial zones, seals, portraits, security threads, watermark details, or anti-counterfeit marks. |
| `rmb-linework-strength` | motif | `subtle-lines` | `subtle-lines`; `balanced-guilloche-inspired`; `linework-off` | Linework must be original generated-vector or code-native geometry and stay below content. |
| `rmb-asset-emphasis` | asset | `manifest-subtle` | `manifest-subtle`; `value-strip`; `corner-frame`; `watermark-panel`; `asset-off` | Use only manifested files under `assets/renminbi_color_style/`; keep them abstract, low-density, and non-counterfeit. |

Preview option behavior:

- `100-yuan-red` uses primary `#BD0E2B`, auxiliary `#F6ACB9`, `#D4606D`, `#E94136`, `#C93649`, and neutral paper/ink colors `#FFFFFF`, `#F6F0E4`, `#241A17`, `#6D716C`.
- Other denomination options map one-to-one to the existing series cards and should be offered as replacements when the user wants a calmer, more compliant, more analytical, or more premium mood.
- `texture-off` keeps RMB style through denomination color progression, fine rules, financial grids, and original geometry.
- Style locks must record the selected denomination series, texture token or `texture-off`, linework strength, selected asset emphasis or `asset-off`, and any rejected counterfeit-like request.

## Self-Check

Return or simulate this `CheckResult` before finishing:

- `ok`: true only when no required fixes remain.
- `issues`: list any concrete RMB style, readability, layout, data, legal-safety, or counterfeit-risk problems.
- `requiredFixes`: list required revisions before delivery.

Minimum checks:

- The design is banknote-inspired but not a currency copy.
- One color family leads; paper, ink, and neutrals carry the reading experience.
- Red and gold are controlled, not overwhelming.
- Numeric information aligns cleanly and remains readable.
- Fine-line decoration does not sit behind dense text, controls, or chart labels.
- Charts use distinguishable colors and do not depend only on red/green.
- UI surfaces use restrained radii, stable spacing tokens, and robust grids.
- Multi-slide or multi-screen work has a value/data/culture visual anchor on every surface, rotates linework/texture/table/chart treatments, and avoids repetitive red-gold metric grids.
- Chinese and English text fit on mobile, desktop, or slide placeholders.
- The design feels trustworthy, valuable, and modern rather than festive, casino-like, or counterfeit.
- No unavailable shared texture provider or real banknote scan is referenced in the output.
