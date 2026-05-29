# Transparent Textures Provider Manifest

This manifest lists the curated `transparent_textures` shared surface provider for `my-design-style`. The canonical upstream source is Transparent Textures (`https://www.transparenttextures.com/`). Assets in this provider are SVG wrappers for high-definition tiled surfaces; each wrapper preserves the upstream PNG source URL and attribution instead of claiming a native SVG source.

| Token | Wrapper file | Attribution | Visual character | Format | SHA-256 |
| --- | --- | --- | --- | --- | --- |
| `textured-paper` | `svg_wrappers/textured-paper.svg` | Stephen Gilbert | soft neutral paper grain with sparse flecks | `svg-wrapper` | `3e8a1cb0f2e8ce745c8055f5a52a7fab643450e70dbf5d90bb57bcfb862176b1` |
| `clean-gray-paper` | `svg_wrappers/clean-gray-paper.svg` | Paul Phönixweiß | clean gray paper grain for restrained institutional surfaces | `svg-wrapper` | `f64241b94c9582f1271edb1a26acd5bd6c9ea691b83c07383a8c29e4e6ccc689` |
| `paper-fibers` | `svg_wrappers/paper-fibers.svg` | Heliodor jalba. | visible paper fibers suitable for tactile cultural and financial backgrounds | `svg-wrapper` | `bc19f5a5a70e503e5b27af72e7aaedf728198921802ca3a9572146f129aaf284` |
| `rice-paper` | `svg_wrappers/rice-paper.svg` | Atle Mo | subtle rice-paper texture for traditional color compositions | `svg-wrapper` | `5cb03fa0d5b49d3cfaa297c282d21e595a3a184e60b76fa08a3029979e3c2e89` |
| `handmade-paper` | `svg_wrappers/handmade-paper.svg` | Le Marquis | organic handmade paper texture for restrained editorial backgrounds | `svg-wrapper` | `6640d41d23ecc3a8bcc653b1178cd9a92af155976b12b2fe19d57a395a87f7ea` |

## Usage Rules

- Use through a concrete style's `SurfaceTexturePolicy`; never browse this provider directly from the base workflow.
- Keep opacity within the active style's `opacityRange`.
- Place textures below content as background, panel, or edge-band substrate only.
- Disable texture when contrast, data readability, legal safety, or brand/identity placement would be harmed.
- Preserve the upstream source URL, creator attribution, and checksum when exporting or transforming a wrapper.
