# Renminbi Color Style Asset Manifest

This manifest is the style-owned asset boundary for `renminbi_color_style`. Import files only through the style's `AssetPolicy`; do not use them from another concrete style.

## Provenance And Use Policy

| Field | Value |
| --- | --- |
| Owner skill | `my-design-style` |
| Concrete style | `renminbi_color_style` |
| Asset role | Optional RMB-inspired abstract linework, corner frames, denomination strips, and financial ornament support. |
| Allowed use | Use only when the active style's asset policy and anti-counterfeit rules permit it. |
| Safety boundary | Keep assets clearly separate from legal tender, official banknote artwork, portraits, serial textures, watermarks, seals, and anti-counterfeit marks. |

## File Inventory

| File | Role | Safe placement | Notes |
| --- | --- | --- | --- |
| _(empty)_ | — | — | No bundled files yet. Add curated assets here with provenance rows before reuse across projects. |

## Import Rules

- An empty inventory is valid. Use code-native geometry, generated vectors, palette progressions, and the `transparent_textures` provider until style-owned files are added.
- Before promoting a downloaded or user-provided file into this boundary, add a manifest row with source URL, license note, SHA-256, role, and safe placement.
- Combine decorative assets as report, dashboard, card, or editorial ornaments rather than voucher, banknote, or security-pattern frames.
