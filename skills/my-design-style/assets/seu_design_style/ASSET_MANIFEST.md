# SEU Asset Manifest

This manifest is the style-owned asset module for `seu_design_style`. Import these assets only through the style's `AssetPolicy`; do not use them from another concrete style.

| File | Role | Size / ratio | Color mode | Safe placement | Notes |
| --- | --- | --- | --- | --- | --- |
| `01_logo_mark_color.svg` | `identity-mark` | 188.977 × 188.909; ratio 1.000 | `color` | `contain` | Compact color mark for agenda side rail, app icon-like identity, or small header anchor. |
| `02_logo_mark_mono.svg` | `identity-mark` | 124.648 × 124.649; ratio 1.000 | `mono` | `contain` | Monochrome compact mark when color would compete with content. |
| `03_wordmark_cn_horizontal.svg` | `wordmark` | 521.575 × 157.31; ratio 3.316 | `mono` | `contain` | Chinese horizontal wordmark for formal identity areas. |
| `04_wordmark_en_horizontal.svg` | `wordmark` | 460.436 × 25.396; ratio 18.130 | `mono` | `contain` | English horizontal wordmark; very wide, use only in spacious header/footer bands. |
| `05_wordmark_cn_vertical.svg` | `wordmark` | 71.6286 × 379.758; ratio 0.189 | `mono` | `contain` | Chinese vertical wordmark for side rails or tall identity blocks. |
| `06_logo_combo_cn_en_horizontal_color.svg` | `logo-lockup` | 511.948 × 157.131; ratio 3.258 | `color` | `contain` | General color header identity. |
| `07_logo_combo_cn_en_horizontal_mono.svg` | `logo-lockup` | 511.949 × 157.132; ratio 3.258 | `mono` | `contain` | General monochrome header identity. |
| `08_logo_combo_cn_horizontal_color.svg` | `logo-lockup` | 511.257 × 146.003; ratio 3.502 | `color` | `contain` | Chinese-only color horizontal identity. |
| `09_logo_combo_cn_horizontal_mono.svg` | `logo-lockup` | 511.257 × 146.004; ratio 3.502 | `mono` | `contain` | Chinese-only monochrome horizontal identity. |
| `10_logo_combo_cn_en_stacked_color.svg` | `logo-lockup` | 317.501 × 316.608; ratio 1.003 | `color` | `contain` | Square-ish color lockup for cover or centered identity block. |
| `11_logo_combo_cn_en_stacked_mono.svg` | `logo-lockup` | 317.501 × 316.61; ratio 1.003 | `mono` | `contain` | Square-ish monochrome lockup. |
| `12_logo_combo_cn_stacked_color.svg` | `logo-lockup` | 317.502 × 282.533; ratio 1.124 | `color` | `contain` | Chinese-only stacked color lockup. |
| `13_logo_combo_cn_stacked_mono.svg` | `logo-lockup` | 317.501 × 282.534; ratio 1.124 | `mono` | `contain` | Chinese-only stacked monochrome lockup. |
| `14_logo_combo_cn_vertical_color.svg` | `logo-lockup` | 105.728 × 478.672; ratio 0.221 | `color` | `contain` | Vertical Chinese color lockup for tall side identity. |
| `15_logo_combo_cn_vertical_mono.svg` | `logo-lockup` | 105.725 × 478.672; ratio 0.221 | `mono` | `contain` | Vertical Chinese monochrome lockup. |
| `16_logo_combo_cn_en_vertical_color.svg` | `logo-lockup` | 151.181 × 532.599; ratio 0.284 | `color` | `contain` | Tall bilingual color lockup for cover or side rail. |
| `17_logo_combo_cn_en_vertical_mono.svg` | `logo-lockup` | 151.181 × 532.599; ratio 0.284 | `mono` | `contain` | Tall bilingual monochrome lockup. |
| `18_color_card.svg` | `color-card` | 67.141 × 137.405; ratio 0.489 | `mixed` | `contain` | Reference color card; use as source evidence, not as decorative filler. |
| `19_motto_horizontal.svg` | `motto` | 365.891 × 85.5331; ratio 4.278 | `mixed` | `contain` | Horizontal motto artwork for closing or formal identity moment. |
| `20_motto_vertical.svg` | `motto` | 93.8808 × 314.137; ratio 0.299 | `mixed` | `contain` | Vertical motto artwork for side rail or content-page ornament. |
| `21_auditorium_single.svg` | `building-silhouette` | 521.575 × 132.211; ratio 3.945 | `mixed` | `contain` | Auditorium single band for closing/header decoration. |
| `22_auditorium_pattern.svg` | `pattern` | 521.575 × 47.9894; ratio 10.869 | `mixed` | `repeatable` | Auditorium repeating pattern for cover/agenda identity texture. |
| `23_auditorium_aux_single.svg` | `building-silhouette` | 412.395 × 150.097; ratio 2.748 | `mixed` | `contain` | Auxiliary auditorium element for right-side or corner ornament. |
| `24_auditorium_aux_pattern.svg` | `pattern` | 412.395 × 50.0329; ratio 8.242 | `mixed` | `repeatable` | Auxiliary pattern for footer/header weak decorative strip. |
| `26_auditorium_silhouette_vertical.svg` | `building-silhouette` | 120.237 × 358.437; ratio 0.335 | `mixed` | `contain` | Vertical auditorium silhouette for section transition anchor. |
| `27_pine.svg` | `botanical-motif` | 228.033 × 385.315; ratio 0.592 | `mixed` | `contain` | Pine motif for closing or cultural identity accent. |

## Import Rules

- Identity marks, wordmarks, motto artwork, building silhouettes, and pine motifs must use contain-style placement.
- Pattern assets marked `repeatable` may repeat or crop while keeping uniform scale.
- The color card is source evidence and should not be placed as filler unless the user asks for a style reference sheet.
- A smaller correctly proportioned identity asset is better than a larger distorted one.
