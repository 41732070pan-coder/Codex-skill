# Transparent Textures Provenance

Provider: `transparent_textures`

Canonical source homepage: `https://www.transparenttextures.com/`

Transparent Textures presents transparent PNG patterns, creator names, download links, and high-definition wallpaper generation controls. The site describes itself as standing on the shoulders of Subtle Patterns and being maintained by `@mikehearn`.

## Acquisition Notes

- Acquisition date: 2026-05-29.
- Network note: the runtime proxy blocked direct binary downloads from `www.transparenttextures.com`, so this provider stores local SVG wrapper files that reference the canonical upstream PNG URLs and capture source metadata. The wrappers are treated as the bundled provider records; the raw upstream PNG binaries are not vendored in this repository.
- Format policy: `sourceFormat: svg-wrapper` means the local file is an SVG tiling wrapper around a Transparent Textures PNG URL; represent wrapper files with that source format rather than as native Transparent Textures SVGs.
- License / terms note: each source page records creator attribution and Subtle Patterns origin. Verify upstream license/terms before redistributing raw PNG binaries or repackaging this provider outside this skill workspace.

## Curated Source Pages

| Token | Source page | PNG source | Attribution |
| --- | --- | --- | --- |
| `textured-paper` | `https://www.transparenttextures.com/textured-paper.html` | `https://www.transparenttextures.com/patterns/textured-paper.png` | Stephen Gilbert |
| `clean-gray-paper` | `https://www.transparenttextures.com/clean-gray-paper.html` | `https://www.transparenttextures.com/patterns/clean-gray-paper.png` | Paul Phönixweiß |
| `paper-fibers` | `https://www.transparenttextures.com/paper-fibers.html` | `https://www.transparenttextures.com/patterns/paper-fibers.png` | Heliodor jalba. |
| `rice-paper` | `https://www.transparenttextures.com/rice-paper.html` | `https://www.transparenttextures.com/patterns/rice-paper.png` | Atle Mo |
| `handmade-paper` | `https://www.transparenttextures.com/handmade-paper.html` | `https://www.transparenttextures.com/patterns/handmade-paper.png` | Le Marquis |
