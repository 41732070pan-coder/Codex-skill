# chinese_traditional_color_style

Use `chinese_traditional_color_style` for designs based on named Chinese traditional colors. It should feel literate, restrained, cultural, and contemporary: a usable design system translated from traditional color names, not an antique poster pasted onto modern UI.

## Contract Conformance

Implements `DesignStyleBase` as `ChineseTraditionalColorStyle`.

Required runtime sections: Triggers, Intent, Anti-Goals, Color Tokens, Typography, Layout Principles, PPT Slide Archetypes, Visual Rhythm System, Web Translation, App / Dashboard Translation, Static Visual Translation, Asset Interface, Surface Texture Policy, Asset Rules, Modifier Compatibility, Preview Option Sets, Self-Check.

Primary references:

- `https://github.com/zerosoul/chinese-colors`: MIT open-source Chinese Color project.
- `https://colors.ichuantong.cn/`: the online Chinese traditional color cheatsheet from that project.
- The project data file `src/assets/colors.json`, which groups colors into 9 source series: red, yellow, green, blue, cang, water, gray-white, black, and gold-silver.

## Triggers

Use this style when the user asks for:

- `chinese_traditional_color_style`, Chinese traditional colors, traditional Chinese palette, Chinese color names.
- 中国传统色, 中式色彩, 古典色彩, 古风配色, 国风配色, 雅致国风, 新中式, 博物馆风, 文物色彩, 宋韵, 东方美学, or similar.
- PPT decks, websites, apps, dashboards, editorial pages, museum or culture pages, brand systems, invitation pages, cultural products, tea, craft, poetry, heritage, or art education.

## Intent

Use the named color system as a disciplined palette source. Each artifact must start from one complete series color card, then apply a compact set of semantic tokens. Color names may add cultural texture, but layout, contrast, hierarchy, and interaction states must stay modern and reliable.

## Anti-Goals

- Do not use every traditional color at once. This is a library, not a confetti system.
- Avoid fake-antique paper, excessive texture, dense frames, seals, clouds, fans, and calligraphy unless the subject truly needs them.
- Avoid illegible pale-on-pale combinations. Many traditional colors are subtle; pair them with ink, white, or controlled deep colors.
- Do not turn UI controls into decorative labels. Buttons, tabs, filters, tables, sliders, and inputs should remain recognizable.
- Avoid large unbroken red/gold festival pages unless the request is explicitly ceremonial.
- Avoid "ancient = serif everywhere." Use serif/Song type as accent, not dense UI body text.

## Color Tokens

Use the named source colors below. Each token maps to a color in the complete source cards.

| Token | Hex | Source Name | Role |
| --- | --- | --- | --- |
| `ct-red-primary` | `#9D2933` | 胭脂 | Formal red primary, titles, strong section identity. |
| `ct-red-bright` | `#FF2121` | 大红 | Ceremonial accent, sparingly. |
| `ct-red-soft` | `#DB5A6B` | 海棠红 | Soft red panels, chart series, selected states. |
| `ct-yellow-primary` | `#FFA631` | 杏黄 | Warm Chinese yellow primary, highlights, cards, commerce. |
| `ct-yellow-gold` | `#EACD76` | 金色 | Metallic accent, small dividers, premium marks. |
| `ct-brown-primary` | `#6E511E` | 褐色 | Grounding, heritage, tea, craft, headings. |
| `ct-green-primary` | `#789262` | 竹青 | Botanical structure, calm navigation, nature/culture. |
| `ct-jade-primary` | `#2EDFA3` | 玉色 | Fresh jade accent, cultural product, icons, success states. |
| `ct-teal-primary` | `#48C0A3` | 青碧 | Fresh teal, links, data, subtle interactive color. |
| `ct-blue-primary` | `#177CB0` | 靛青 | Analytical blue, content links, data surfaces. |
| `ct-blue-deep` | `#065279` | 靛蓝 | Deep header, navigation, contrast blocks. |
| `ct-purple-primary` | `#8D4BBB` | 紫色 | Poetic/premium accent, cultural editorial. |
| `ct-cang-primary` | `#75878A` | 苍色 | Muted gray-blue system color, panels, quiet UI chrome. |
| `ct-water-primary` | `#D2F0F4` | 水蓝 | Pale water background, airy sections. |
| `ct-white-primary` | `#FFFBF0` | 象牙白 | Warm surface, document/paper background. |
| `ct-black-primary` | `#161823` | 漆黑 | Main ink, high contrast, dark mode anchor. |
| `ct-ink-soft` | `#50616D` | 墨色 | Body text, secondary dark UI. |
| `ct-silver-primary` | `#BACAC6` | 老银 | Metallic neutral, borders, quiet data. |

Suggested UI token mapping:

```css
:root {
  --ct-red-primary: #9d2933;
  --ct-red-bright: #ff2121;
  --ct-red-soft: #db5a6b;
  --ct-yellow-primary: #ffa631;
  --ct-yellow-gold: #eacd76;
  --ct-brown-primary: #6e511e;
  --ct-green-primary: #789262;
  --ct-jade-primary: #2edfa3;
  --ct-teal-primary: #48c0a3;
  --ct-blue-primary: #177cb0;
  --ct-blue-deep: #065279;
  --ct-purple-primary: #8d4bbb;
  --ct-cang-primary: #75878a;
  --ct-water-primary: #d2f0f4;
  --ct-white-primary: #fffbf0;
  --ct-black-primary: #161823;
  --ct-ink-soft: #50616d;
  --ct-silver-primary: #bacac6;
  --surface: #fffbf0;
  --surface-clean: #ffffff;
  --surface-soft: #f2ecde;
  --border-subtle: rgba(22, 24, 35, 0.14);
  --text: #161823;
  --text-mid: rgba(22, 24, 35, 0.72);
  --text-weak: rgba(22, 24, 35, 0.52);
}
```

## Series Color Cards

Every design using this style must start from at least one complete series color card. Use the series primary as the lead and the listed colors as auxiliary choices. If no cultural palette direction is given, use `Default Ink Paper Fallback`.

Hard requirements:

- Do not invent colors for this style when a matching source color exists.
- Preserve every color name and HEX value from the complete source cards.
- Treat each source series as a full card: one primary plus all remaining colors as auxiliary colors.
- For implementation tokens, use the stable source-token format below so every color can be addressed without ad hoc pinyin.
- If a requested artifact needs a color outside the source cards, use `Default Ink Paper Fallback` neutrals before adding any non-source color.
- Follow the shared same-family progression model in `design_mechanics.md`: primary, support-strong, support-mid, support-soft, wash, muted-bridge.

### Stable Source Tokens

Every color in the complete source cards can be converted into a deterministic token:

```text
--ct-src-<series-id>-<color-id>
```

Use the source IDs from `colors.json`: red `0`, yellow `1`, green `2`, blue `3`, cang `4`, water `5`, gray-white `6`, black `7`, gold-silver `8`.

Examples:

| Source Color | Stable Token | Hex |
| --- | --- | --- |
| 胭脂 | `--ct-src-0-11` | `#9D2933` |
| 杏黄 | `--ct-src-1-3` | `#FFA631` |
| 竹青 | `--ct-src-2-3` | `#789262` |
| 靛青 | `--ct-src-3-1` | `#177CB0` |
| 苍色 | `--ct-src-4-0` | `#75878A` |
| 水蓝 | `--ct-src-5-3` | `#D2F0F4` |
| 象牙白 | `--ct-src-6-1` | `#FFFBF0` |
| 漆黑 | `--ct-src-7-4` | `#161823` |
| 金色 | `--ct-src-8-1` | `#EACD76` |

When creating CSS or design-token files, include only the tokens used by the artifact plus the selected card. For color-library views, include every token in the selected source series.

### Curated Working Cards

These cards are optimized for actual PPT/UI work and are drawn from the complete source cards below.

| Series | Primary | Auxiliary Colors | Neutral / Base | Use |
| --- | --- | --- | --- | --- |
| Rouge Ceremony | 胭脂 `#9D2933` | 粉红 `#FFB3A7`, 海棠红 `#DB5A6B`, 朱红 `#FF4C00`, 殷红 `#BE002F` | 象牙白 `#FFFBF0`, 墨色 `#50616D`, 漆黑 `#161823` | Festival, culture brand, titles, formal deck covers. |
| Apricot Gold | 杏黄 `#FFA631` | 鹅黄 `#FFF143`, 姜黄 `#FFC773`, 缃色 `#F0C239`, 秋香色 `#D9B611` | 象牙白 `#FFFBF0`, 褐色 `#6E511E`, 墨色 `#50616D` | Commerce, craft, tea, warm reports, premium highlights. |
| Bamboo Jade | 竹青 `#789262` | 柳绿 `#AFDD22`, 青葱 `#0AA344`, 玉色 `#2EDFA3`, 松柏绿 `#21A675` | 素 `#E0F0E9`, 漆黑 `#161823`, 墨色 `#50616D` | Botanical, wellness, education, calm cultural UI. |
| Indigo Scholarly | 靛青 `#177CB0` | 蓝 `#44CEF6`, 靛蓝 `#065279`, 宝蓝 `#4B5CC4`, 蓝灰色 `#A1AFC9` | 月白 `#D6ECF0`, 象牙白 `#FFFBF0`, 漆黑 `#161823` | Knowledge, museum data, analysis, scholarly pages. |
| Purple Poetry | 紫色 `#8D4BBB` | 黛紫 `#574266`, 青莲 `#801DAE`, 雪青 `#B0A4E3`, 丁香色 `#CCA4E3` | 藕色 `#EDD1D8`, 象牙白 `#FFFBF0`, 漆黑 `#161823` | Poetry, arts, premium cultural editorial. |
| Cang Mountain | 苍色 `#75878A` | 苍翠 `#519A73`, 苍黄 `#A29B7C`, 苍青 `#7397AB`, 苍黑 `#395260` | 苍白 `#D1D9E0`, 象牙白 `#FFFBF0`, 墨色 `#50616D` | Landscape, documentary, restrained dashboards. |
| Water Moon | 水蓝 `#D2F0F4` | 水色 `#88ADA6`, 水红 `#F3D3E7`, 水绿 `#D4F2E7`, 湖蓝 `#30DFF3` | 雪白 `#F2FDFF`, 墨色 `#50616D`, 漆黑 `#161823` | Light pages, poetry, wellness, airy product UI. |
| Ink Paper | 漆黑 `#161823` | 玄青 `#3D3B4F`, 墨色 `#50616D`, 墨灰 `#758A99`, 黎 `#5D513C` | 精白 `#FFFFFF`, 象牙白 `#FFFBF0`, 铅白 `#F0F0F4` | Documents, dashboards, formal typography, high contrast. |
| Gold Silver | 金色 `#EACD76` | 赤金 `#F2BE45`, 银白 `#E9E7EF`, 老银 `#BACAC6`, 铜绿 `#549688` | 象牙白 `#FFFBF0`, 漆黑 `#161823`, 墨色 `#50616D` | Premium, craft, jewelry, museum object pages. |
| Default Ink Paper Fallback | 漆黑 `#161823` | 精白 `#FFFFFF`, 象牙白 `#FFFBF0`, 灰色 `#808080`, 墨色 `#50616D` | `#FFFFFF`, `#F5F5F5`, `#161823`, `#808080` | Use only when no traditional color family should lead. |

### Same-Family Progression Cards

Use these cards when a user asks for one dominant hue family. The primary color defines identity; the support colors create RMB-like gradation for secondary emphasis, chart companions, transition panels, and non-primary highlighted content.

| Family | Primary | Support-Strong | Support-Mid | Support-Soft | Wash | Muted-Bridge | Use |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Rouge Progression | 胭脂 `#9D2933` | 殷红 `#BE002F` | 海棠红 `#DB5A6B` | 嫣红 `#EF7A82` | 粉红 `#FFB3A7` | 檀 `#B36D61` | Formal red family, chapter emphasis, selected state, culture brand. |
| Apricot Progression | 杏黄 `#FFA631` | 黄栌 `#E29C45` | 姜黄 `#FFC773` | 枯黄 `#D3B17D` | 牙色 `#EEDEB0` | 褐色 `#6E511E` | Warm commerce, craft, tea, premium cultural reports. |
| Bamboo Progression | 竹青 `#789262` | 青葱 `#0AA344` | 松柏绿 `#21A675` | 石青 `#7BCFA6` | 素 `#E0F0E9` | 鸦青 `#424C50` | Botanical, wellness, education, calm cultural UI. |
| Indigo Progression | 靛青 `#177CB0` | 靛蓝 `#065279` | 群青 `#4C8DAE` | 蓝灰色 `#A1AFC9` | 月白 `#D6ECF0` | 藏青 `#2E4E7E` | Knowledge, museum data, analysis, scholarly pages. |
| Purple Progression | 紫色 `#8D4BBB` | 青莲 `#801DAE` | 雪青 `#B0A4E3` | 丁香色 `#CCA4E3` | 藕色 `#EDD1D8` | 黛紫 `#574266` | Poetry, arts, premium cultural editorial. |
| Cang Progression | 苍色 `#75878A` | 苍黑 `#395260` | 苍青 `#7397AB` | 苍白 `#D1D9E0` | 霜色 `#E9F1F6` | 苍黄 `#A29B7C` | Landscape, archive, documentary, restrained dashboards. |

### Complete Source Color Cards

These tables preserve every color from the referenced `colors.json`. Keep names and HEX values intact when using the source colors.

| Source Series | Primary | Complete Color Card |
| --- | --- | --- |
| 红 | `#FFB3A7` | 粉红 `#FFB3A7`, 妃色 `#ED5736`, 品红 `#F00056`, 桃红 `#F47983`, 海棠红 `#DB5A6B`, 石榴红 `#F20C00`, 樱桃色 `#C93756`, 银红 `#F05654`, 大红 `#FF2121`, 绛紫 `#8C4356`, 绯红 `#C83C23`, 胭脂 `#9D2933`, 朱红 `#FF4C00`, 丹 `#FF4E20`, 彤 `#F35336`, 茜色 `#CB3A56`, 火红 `#FF2D51`, 赫赤 `#C91F37`, 嫣红 `#EF7A82`, 洋红 `#FF0097`, 炎 `#FF3300`, 赤 `#C3272B`, 绾 `#A98175`, 枣红 `#C32136`, 檀 `#B36D61`, 殷红 `#BE002F`, 酡红 `#DC3023`, 酡颜 `#F9906F` |
| 黄 | `#FFF143` | 鹅黄 `#FFF143`, 鸭黄 `#FAFF72`, 樱草色 `#EAFF56`, 杏黄 `#FFA631`, 杏红 `#FF8C31`, 橘黄 `#FF8936`, 橙黄 `#FFA400`, 橘红 `#FF7500`, 姜黄 `#FFC773`, 缃色 `#F0C239`, 橙色 `#FA8C35`, 茶色 `#B35C44`, 驼色 `#A88462`, 昏黄 `#C89B40`, 栗色 `#60281E`, 棕色 `#B25D25`, 棕绿 `#827100`, 棕黑 `#7C4B00`, 棕红 `#9B4400`, 棕黄 `#AE7000`, 赭 `#9C5333`, 赭色 `#955539`, 琥珀 `#CA6924`, 褐色 `#6E511E`, 枯黄 `#D3B17D`, 黄栌 `#E29C45`, 秋色 `#896C39`, 秋香色 `#D9B611` |
| 绿 | `#0AA344` | 嫩绿 `#BDDD22`, 柳黄 `#C9DD22`, 柳绿 `#AFDD22`, 竹青 `#789262`, 葱黄 `#A3D900`, 葱绿 `#9ED900`, 葱青 `#0EB83A`, 葱倩 `#0EB840`, 青葱 `#0AA344`, 油绿 `#00BC12`, 绿沈 `#0C8918`, 碧色 `#1BD1A5`, 碧绿 `#2ADD9C`, 青碧 `#48C0A3`, 翡翠色 `#3DE1AD`, 草绿 `#40DE5A`, 青色 `#00E09E`, 青翠 `#00E079`, 青白 `#C0EBD7`, 鸭卵青 `#E0EEE8`, 蟹壳青 `#BBCDC5`, 鸦青 `#424C50`, 绿色 `#00E500`, 豆绿 `#9ED048`, 豆青 `#96CE54`, 石青 `#7BCFA6`, 玉色 `#2EDFA3`, 缥 `#7FECAD`, 艾绿 `#A4E2C6`, 松柏绿 `#21A675`, 松花绿 `#057748`, 松花色 `#BCE672` |
| 蓝 | `#44CEF6` | 蓝 `#44CEF6`, 靛青 `#177CB0`, 靛蓝 `#065279`, 碧蓝 `#3EEDE7`, 蔚蓝 `#70F3FF`, 宝蓝 `#4B5CC4`, 蓝灰色 `#A1AFC9`, 藏青 `#2E4E7E`, 藏蓝 `#3B2E7E`, 黛 `#4A4266`, 黛绿 `#426666`, 黛蓝 `#425066`, 黛紫 `#574266`, 紫色 `#8D4BBB`, 紫酱 `#815463`, 酱紫 `#815476`, 紫檀 `#4C221B`, 绀青 `#003371`, 紫棠 `#56004F`, 青莲 `#801DAE`, 群青 `#4C8DAE`, 雪青 `#B0A4E3`, 丁香色 `#CCA4E3`, 藕色 `#EDD1D8`, 藕荷色 `#E4C6D0` |
| 苍 | `#75878A` | 苍色 `#75878A`, 苍翠 `#519A73`, 苍黄 `#A29B7C`, 苍青 `#7397AB`, 苍黑 `#395260`, 苍白 `#D1D9E0` |
| 水 | `#D2F0F4` | 水色 `#88ADA6`, 水红 `#F3D3E7`, 水绿 `#D4F2E7`, 水蓝 `#D2F0F4`, 淡青 `#D3E0F3`, 湖蓝 `#30DFF3`, 湖绿 `#25F8CB` |
| 灰白 | `#F0F0F4` | 精白 `#FFFFFF`, 象牙白 `#FFFBF0`, 雪白 `#F2FDFF`, 月白 `#D6ECF0`, 缟 `#F2ECDE`, 素 `#E0F0E9`, 荼白 `#F3F9F1`, 霜色 `#E9F1F6`, 花白 `#C2CCD0`, 鱼肚白 `#FCEFE8`, 莹白 `#E3F9FD`, 灰色 `#808080`, 牙色 `#EEDEB0`, 铅白 `#F0F0F4` |
| 黑 | `#000000` | 玄色 `#622A1D`, 玄青 `#3D3B4F`, 乌色 `#725E82`, 乌黑 `#392F41`, 漆黑 `#161823`, 墨色 `#50616D`, 墨灰 `#758A99`, 黑色 `#000000`, 缁色 `#493131`, 煤黑 `#312520`, 黎 `#5D513C`, 黝 `#75664D`, 黝青 `#6B6882`, 黝黑 `#665757`, 黯 `#41555D` |
| 金银 | `#EACD76` | 赤金 `#F2BE45`, 金色 `#EACD76`, 银白 `#E9E7EF`, 老银 `#BACAC6`, 乌金 `#A78E44`, 铜绿 `#549688` |

## Palette Recipes

Use one primary card per artifact, then add only one optional secondary card.

| Recipe | Palette | Use |
| --- | --- | --- |
| Museum Calm | `Indigo Scholarly` + `Ink Paper` | Exhibition pages, object records, cultural dashboards. |
| Poetic Editorial | `Purple Poetry` + `Water Moon` | Literature, poetry, arts, invitation pages. |
| Craft Warmth | `Apricot Gold` + `Gold Silver` | Tea, craft, commerce, luxury cultural goods. |
| Botanical Study | `Bamboo Jade` + `Ink Paper` | Nature education, wellness, botanical products. |
| Ceremony Accent | `Rouge Ceremony` + `Apricot Gold` | Formal covers, festival identity, keynote openings. |
| Landscape Archive | `Cang Mountain` + `Ink Paper` | Documentary, archive, heritage, serious reports. |

For charts, choose colors from one complete source series first; add a second series only when categories exceed 5-6 values. Use color names in legends when useful, but keep legends compact.

## Typography

- Prefer modern Chinese sans-serif for UI and dense content: Source Han Sans SC, Noto Sans CJK SC, Microsoft YaHei, PingFang SC, HarmonyOS Sans.
- Use Song/Ming type for large editorial titles, quotations, covers, museum labels, or chapter transitions: Source Han Serif SC, Noto Serif CJK SC, SimSun fallback.
- Keep body text readable and modern. Traditional colors carry the cultural tone; typography should not become costume.
- Use tabular numerals for dashboards, dates, inventory IDs, catalog numbers, and chart labels.
- Chinese color names may appear as small labels, chips, swatches, or section markers. Do not overuse vertical text unless the layout is explicitly editorial.

## Layout Principles

- Use the same progressive, reference-driven structure as robust design-system documentation: tokens first, then components, then page patterns, then validation.
- Build on stable grids: 12-column web grids, 8px spacing increments, and fixed comparison columns for dashboards and tables.
- For PPT, use generous margins, clear title/content zones, and repeatable archetypes; never rely on decorative absolute positioning for the main information.
- Use decorative cultural motifs as surface texture or edge structure only: fine rules, seal-like square markers, book margins, gallery labels, scroll-inspired vertical rails.
- Keep cards to individual repeated objects or tools. Avoid nested cards and heavy ornamental frames.
- Pair subtle colors with deep ink. Pale traditional colors need contrast from `ct-black-primary`, `ct-ink-soft`, or white surfaces.
- For dense interfaces, reduce ornament density and use color mainly for navigation state, category, risk, charts, and selected rows.

## Documentation / Composition Model

Follow the same information architecture used by strong skills and mature design systems:

- Start with intent and anti-goals so later design choices do not drift into decoration.
- Put color tokens and complete source cards before layout recipes, because this style is color-library driven.
- Separate reusable working cards from complete source inventory: working cards guide everyday design, complete cards preserve the full source.
- Describe components by role and state, not by ornamental appearance. A button is still a button; a chart is still a chart.
- Use repeatable page archetypes for PPT and web/app surfaces, similar to high-quality design system docs that move from tokens to components to patterns.
- Validate visually at the end: alignment, contrast, text overflow, responsive behavior, chart legibility, and whether cultural motifs support content.

## PPT Slide Archetypes

| Archetype | Purpose | Style notes |
| --- | --- | --- |
| Cover | Title, subtitle, organization, date | One dominant series card; large Song/Ming title acceptable; minimal line ornament. |
| Color Legend | Introduce chosen palette | Show swatches with Chinese names and HEX; include usage roles, not just decoration. |
| Agenda | 3-6 sections | Use series colors as section markers; keep text in ink. |
| Section Transition | Chapter break | Large color field or pale wash; one strong title and optional source color name. |
| Object / Artifact | Museum or product item | Image area, metadata column, quiet label system, restrained color accent. |
| Editorial Text | Essay, context, story | Song/Ming heading, sans-serif body, wide margins, short pull quote. |
| Data / Chart | Research or dashboard result | Use chart colors from one source series; avoid low-contrast pale values for thin lines. |
| Comparison Table | Methods, objects, brands, variants | Stable columns, soft separators, color chips only where they encode meaning. |
| Closing | Thanks, source, contact | Return to chosen primary card and ink/paper base. |

For slide decks, use 16:9 by default.

## Visual Rhythm System

Use a deck-level visual rhythm plan so traditional color work feels restrained but not empty. 克制 does not mean blank; it means low-density, explainable visual gestures that serve structure.

- `rhythmScope`: for PPT decks, assign every slide to a content archetype before drawing; for web/app work, assign each major section to a museum, editorial, catalog, dashboard, or component role.
- `visualAnchorRule`: every slide or major section needs one non-body-text anchor: named-color swatch strip, color chip matrix, diagram, comparison table, gallery label, book rail, seal-like dot, fine-rule frame, quote block, lawful image, or low-opacity paper texture.
- `archetypeVarietyRule`: no more than two consecutive slides should use the same title/body skeleton; alternate cover/agenda, color legend, concept diagram, data/table, editorial/object, and closing patterns.
- `motifRotation`: rotate restrained-rules, gallery-labels, seal-dot-accents, book rails, swatch strips, texture-off states, and motif-off for dense data; never add clouds, fans, lanterns, dragons, or calligraphy as filler.
- `assetFallbackRule`: use bundled borders/stripes/placeholders when they fit the content, plus code-native geometry, color swatches, typographic labels, diagrams, and approved texture tokens before leaving large empty zones.
- `antiMonotonyCheck`: confirm that each page has a visible anchor beyond body text, at least three approved motif treatments appear across decks longer than six slides, and decoration supports hierarchy rather than filling space.

## Web Translation

For websites, build the actual experience first: museum object page, brand system, catalog, dashboard, article, education module, commerce product page, or cultural landing section.

Use:

- A restrained header with ink text and one series-color active mark.
- Color swatches with names and HEX when the artifact is about color or design.
- Real imagery, artwork, product photography, object scans, or generated bitmap visuals when a hero is needed.
- Pale source colors for backgrounds; deeper colors for text anchors, navigation, chart series, and buttons.
- Clear component states: hover, active, selected, disabled, error, success.
- Small cultural gestures: square markers, thin vertical rails, caption blocks, seal-red active dots, fine separators.

Avoid:

- Full-screen abstract gradient pages.
- Dark, blurred, stock-like images when the object or cultural subject should be inspectable.
- Text over high-detail texture.
- Oversized decorative hero cards instead of useful content.

## App / Dashboard Translation

Use a quiet cultural-operations feel:

- Navigation should be compact and scannable; active state can use one traditional color plus a shape/icon.
- Tables, filters, tabs, segmented controls, and charts must remain conventional and accessible.
- Use color chips for categories, collections, dynasties, artifact materials, inventory states, or content status.
- Do not rely only on red/green status. Pair color with label, icon, or shape.
- Use `Ink Paper`, `Cang Mountain`, or `Indigo Scholarly` as default dashboard bases; add other cards for category systems.
- Check responsive text carefully: Chinese color names and cultural labels must not overlap buttons, cards, or table columns.

## Static Visual Translation

For posters, title cards, diagrams, thumbnails, or cultural static visuals:

- Select one named traditional color card before composing the visual.
- Use generous margins, book-like framing, restrained swatches, and modern grid structure.
- Keep cultural motifs secondary to the message; avoid generic seals, clouds, dragons, lanterns, or calligraphy filler.
- Pair pale traditional colors with strong ink text for readability.
- Use Chinese color names and HEX labels only when they add explanatory value.

## Asset Interface

This style exposes a small style-owned SVG asset module for restrained guofeng borders, stripes, side bands, and placeholder imagery.

- `assetRoot`: `assets/chinese_traditional_color_style/`.
- `importMode`: `manifested-svg`.
- `manifestFile`: `assets/chinese_traditional_color_style/ASSET_MANIFEST.md`.
- `availableAssets`: `guofeng_border_frame`, `cloud_lattice_stripe`, `landscape_placeholder`, `vertical_pattern_band`.
- `usageRoles`: named color cards, border frames, horizontal stripes, vertical pattern bands, placeholder image panels, user-provided cultural imagery, generated bitmap visuals, color swatches, lawful object imagery, and small code-native motifs.
- `placementRules`: preserve aspect ratio; crop only declared stripes/bands at their ends; keep cultural imagery secondary to content unless the artifact is explicitly an object, museum, or editorial view; keep motifs low-density and away from dense text.
- `fallbackPolicy`: use named color cards, ink/paper contrast, typography, grid, code-native geometry, and bundled manifest assets instead of borrowing assets from another concrete style.

When an artifact needs Chinese traditional visual material:

- Use `01_guofeng_border_frame.svg` for title cards, chapter pages, posters, and museum-style labels when a border is useful.
- Use `02_cloud_lattice_stripe.svg` and `04_vertical_pattern_band.svg` as sparse page rhythm devices; do not stack them on every page.
- Use `03_landscape_placeholder.svg` only as a temporary placeholder when final user-provided photography, object imagery, or illustration is not available.
- For PPT/UI structure, prefer clean layout, restrained color, typography, thin rules, tabs, tables, and code-native geometry over ornamental filler.
- Do not assume every Chinese theme needs dragons, clouds, seals, folding fans, mountains, or calligraphy.
- Prefer color, whitespace, text hierarchy, and composition over decorative symbolism.

## Surface Texture Policy

Traditional-color texture support is enabled through the bundled `transparent_textures` provider for restrained paper tactility behind named-color systems and contemporary cultural composition.

- `provider`: `transparent_textures`
- `assetRoot`: `assets/transparent_textures/`
- `manifestFile`: `assets/transparent_textures/TEXTURE_MANIFEST.md`
- `indexFile`: `assets/transparent_textures/texture_index.json`
- `provenanceFile`: `assets/transparent_textures/provenance.md`
- `defaultToken`: `rice-paper`
- `allowedTokens`: ["rice-paper", "paper-fibers", "handmade-paper", "textured-paper"]
- `opacityRange`: [0.03, 0.08]
- `allowedSurfaces`: ["page-background", "museum-panel", "cover-wash", "editorial-background"]
- `forbiddenSurfaces`: ["dense body text", "color-swatch labels", "small museum metadata", "chart labels", "generated calligraphy", "seal-like marks"]
- `fallbackPolicy`: disable texture and keep the style through named color cards, ink/paper contrast, typography, margins, fine rules, and code-native geometry.

Texture must not make the artifact fake-antique or reduce legibility.

## Asset Rules

Bundled assets are available under `assets/chinese_traditional_color_style/` and must be selected through `ASSET_MANIFEST.md`.

Allowed:

- Manifested style-owned assets: `01_guofeng_border_frame.svg`, `02_cloud_lattice_stripe.svg`, `03_landscape_placeholder.svg`, and `04_vertical_pattern_band.svg`.
- Original or lawfully sourced cultural imagery, museum objects, textiles, ceramics, landscapes, ink textures, paper texture, or generated raster visuals.
- CSS/SVG fine-line patterns, seal-like geometry, book margin rails, quiet texture, and swatches.
- Color chips named with Chinese color names and HEX.

Avoid:

- Copying copyrighted artwork or museum photography without permission.
- Low-resolution decorative textures that make text blurry.
- Overusing seals, clouds, dragons, fans, lanterns, or calligraphy as filler.

## Modifier Compatibility

Chinese traditional color modifiers are supported when they preserve the named-color discipline, cultural restraint, contrast, and modern component usability of the base style. Use modifiers to tune a selected color-series plan, not to turn the artifact into generic ornament.

- `acceptsModifiers`: true.
- `allowedTargets`: palette, motif, texture, layout, mood, asset.
- `allowedSources`: style-owned when declared, user-provided, generated-vector, code-native, shared-provider only when explicitly enabled by the surface policy, and none.
- `defaultIntensity`: subtle for app/dashboard work, balanced for editorial, cultural, or PPT section pages.
- `conflictPolicy`: preserve named source colors, readable ink/surface contrast, and modern component roles; downgrade or reject modifiers that create confetti palettes, fake-antique clutter, or illegible pale-on-pale layouts.
- `promotionPolicy`: promote recurring named variants such as Song editorial, museum object, tea craft, or festival ceremony modes into concrete styles only when they need durable palette recipes, assets, registry metadata, or validators.

Hard invariants:

- Start from one complete source series or documented palette recipe; do not mix many unrelated traditional colors just because they are available.
- Keep cultural motifs secondary to content, navigation, data, and component states.
- Preserve contrast by pairing pale colors with ink, white, or controlled deep colors.
- Do not make UI controls unrecognizable through ornamental labels, frames, or excessive calligraphy.

Allowed soft modifiers:

- Mood or seasonal adjustments that select a different source series or add one controlled accent.
- Generated-vector or code-native cultural gestures such as thin rules, square markers, gallery labels, scroll-like rails, or seal-like dots when they stay low density.
- User-provided imagery, object photos, or cultural assets when provenance is acceptable and placement supports the content.
- Layout-density adjustments for editorial, museum, dashboard, or product contexts while preserving stable grids.

Modifier self-check additions:

- The result still uses named-color logic rather than a generic red/gold or antique palette.
- Added motifs are restrained and do not crowd body text, controls, charts, or object metadata.
- Pale modifiers maintain readable contrast.
- Any recurring expressive modifier is identified as a candidate concrete style rather than silently becoming the base style.

## Preview Option Sets

`getPreviewOptions(request, composedPlan)` exposes preview choices. In `previewMode: auto`, explicit preview is used only when ambiguity, stakes, cultural sensitivity, brand sensitivity, or user request requires it. Otherwise the model creates an internal `StyleLock` from the default option sets and proceeds. When a preview is used, it should show the selected named-color series, ink/paper contrast, typography hierarchy, restrained cultural component samples, and any paper texture. `applyStyleLock(styleLock, composedPlan)` must preserve the locked source color series, texture, motif restraint, and layout density in the final artifact.

| Option Set | Target | Default | Options | Rules |
| --- | --- | --- | --- | --- |
| `traditional-color-series` | palette | context-dependent named source series or documented palette recipe | selected source series; adjacent source series; documented recipe; neutral ink-paper fallback | Start from one complete named-color logic; avoid mixing many unrelated traditional colors. |
| `traditional-paper-texture` | texture | `rice-paper` | `rice-paper`; `paper-fibers`; `handmade-paper`; `textured-paper`; `texture-off` | Tokens must come from `allowedTokens`; keep opacity in `[0.03, 0.08]`; never weaken swatch labels, metadata, chart labels, or generated calligraphy. |
| `cultural-motif-level` | motif | `restrained-rules` | `restrained-rules`; `gallery-labels`; `seal-dot-accents`; `motif-off` | Motifs stay low-density, code-native or generated-vector, and never become generic antique filler. |
| `traditional-asset-emphasis` | asset | `manifest-subtle` | `manifest-subtle`; `border-frame`; `lattice-stripe`; `image-placeholder`; `vertical-band`; `asset-off` | Use only manifested files under `assets/chinese_traditional_color_style/`; keep one clear asset role per surface. |

Preview option behavior:

- Texture choices are paper tactility only; they must not make the artifact fake-antique.
- `texture-off` preserves the style through named colors, ink/paper contrast, margins, fine rules, and modern component structure.
- Style locks must record the selected color series or recipe, texture token or `texture-off`, motif level, selected asset emphasis or `asset-off`, layout density, and any downgraded expressive modifier.

## Self-Check

Return or simulate this `CheckResult` before finishing:

- `ok`: true only when no required fixes remain.
- `issues`: list any concrete color-card, cultural-context, readability, layout, asset, or medium-specific problems.
- `requiredFixes`: list required revisions before delivery.

Minimum checks:

- A complete series color card was selected before designing.
- All used colors come from the named cards or the neutral fallback.
- The design uses no more than one primary card plus one secondary card unless it is a color-library view.
- Text contrast is strong enough on pale traditional colors.
- Cultural decoration supports hierarchy rather than filling empty space.
- The layout is modern, grid-based, and content-first.
- Multi-slide or multi-screen work has a visual anchor on every surface, rotates approved restrained motifs, and avoids both blank pages and ornamental filler.
- Tables, charts, and UI controls remain recognizable and usable.
- Chinese color names and HEX labels fit without overlap.
- The artifact feels Chinese and refined without becoming fake-antique or festive by default.
- No unavailable shared texture provider is referenced in the output.
