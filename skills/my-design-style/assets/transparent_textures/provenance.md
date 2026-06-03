# Transparent Textures Provenance

Provider: `transparent_textures`

Inspiration homepage: `https://www.transparenttextures.com/`

This provider bundles 42 seamless textures inspired by the Transparent Textures pattern library. The token vocabulary spans paper, fabric, grunge, wood, metal, and geometric families so concrete styles can pick a substrate that fits their identity.

## Implementation Notes

- Format policy: each token is a **self-contained SVG** under `svg_wrappers/`. Most are `svg-inlined-png` — a seamless PNG tile encoded as a base64 `data:` URI inside an SVG `<pattern>`. One (`paper-fibers`) is `svg-procedural`, generated at render time with `feTurbulence`.
- No remote dependency: there is no `<image href="https://…">` anywhere. This was a deliberate fix — earlier remote-href wrappers rendered blank offline/headless, so styles silently fell back to `texture-off`. `validate_styles.py` now rejects any remote href in a provider wrapper.
- Offline-safe: every wrapper renders identically offline, behind a proxy, and in headless SVG-to-bitmap export (PPT/PDF/PNG pipelines).
- Tunable: inlined tiles can be recolored with an overlay or `feColorMatrix`; the procedural token exposes `baseFrequency`/`numOctaves`/`seed`.
- Acquisition: source PNG tiles were downloaded once from `transparenttextures.com/patterns/<slug>.png` and inlined; the raw PNGs are not vendored separately.

## Token Inspiration

| Token | Category | Inspired by pattern (original author) |
| --- | --- | --- |
| `beige-paper` | paper | 'Beige Paper' by Atle Mo |
| `cardboard` | paper | 'Cardboard' by Jordan Pittman |
| `clean-gray-paper` | paper | 'Clean Gray Paper' by Paul Phönixweiß |
| `handmade-paper` | paper | 'Handmade Paper' by Le Marquis |
| `light-paper-fibers` | paper | 'Light Paper Fibers' by Tertius A. Anjos |
| `lined-paper` | paper | 'Lined Paper' by Mahdesign |
| `natural-paper` | paper | 'Natural Paper' by Daniel Beaton |
| `paper-fibers` | paper | 'Paper Fibers' by Heliodor jalba. |
| `rice-paper` | paper | 'Rice Paper' by Atle Mo |
| `textured-paper` | paper | 'Textured Paper' by Stephen Gilbert |
| `black-linen` | fabric | 'Black Linen' by Sukic |
| `fabric-of-squares` | fabric | 'Fabric Of Squares' by Dmitry |
| `fabric-plaid` | fabric | 'Fabric Plaid' by Peax |
| `leather` | fabric | 'Leather' by Elemis |
| `low-contrast-linen` | fabric | 'Low Contrast Linen' by Adam Pickering |
| `asfalt-light` | grunge | 'Asfalt Light' by Tsvetelin Nikolov |
| `brick-wall` | grunge | 'Brick Wall' by Wassim |
| `concrete-wall` | grunge | 'Concrete Wall' by Anatoli Nicolae |
| `dust` | grunge | 'Dust' by Cd Cf |
| `rocky-wall` | grunge | 'Rocky Wall' by Projecteightyfive |
| `shattered` | grunge | 'Shattered' by Daniel Beaton |
| `vintage-speckles` | grunge | 'Vintage Speckles' by Vinny Vibes |
| `dark-wood` | wood | 'Dark Wood' by Andreas Larsson |
| `purty-wood` | wood | 'Purty Wood' by Tim Ribchester |
| `retina-wood` | wood | 'Retina Wood' by Adam Pickering |
| `wood-pattern` | wood | 'Wood Pattern' by Shahid |
| `brushed-alum` | metal | 'Brushed Aluminium' by Tsvetelin Nikolov |
| `gold-scale` | metal | 'Gold Scale' by Tony Kinard |
| `3px-tile` | geometric | '3px Tile' by Mizan |
| `batthern` | geometric | 'Batthern' by Christopher Buecheler |
| `cubes` | geometric | 'Cubes' by Mike Hearn |
| `diagmonds` | geometric | 'Diagmonds' by Christopher Burton |
| `gplay` | geometric | 'Gplay' by Alex Parker |
| `gray-floral` | geometric | 'Gray Floral' by Tontuf |
| `hexellence` | geometric | 'Hexellence' by Atle Mo |
| `maze-white` | geometric | 'Maze White' by Peax |
| `otis-redding` | geometric | 'Otis Redding' by Listvetra |
| `pinstripe-light` | geometric | 'Pinstripe Light' by Webdesignerdepot |
| `pyramid` | geometric | 'Pyramid' by Subtle Patterns |
| `stardust` | geometric | 'Stardust' by Atle Mo |
| `subtle-white-feathers` | geometric | 'Subtle White Feathers' by Josh Green |
| `white-diamond` | geometric | 'White Diamond' by Power |
