---
name: my-design-style
description: Extensible visual design framework for PPT decks, websites, apps, dashboards, frontend demos, and static visual assets. Use when Codex needs to apply or extend a named house style such as seu_design_style, renminbi_color_style, or chinese_traditional_color_style while preserving shared style contracts, asset boundaries, and quality gates.
---

# My Design Style

## Purpose

Use this skill to translate a target artifact into one named visual style from the `my-design-style` family. Treat the skill as a compact design framework: `SKILL.md` owns dispatch and invariants; references own contracts, registries, templates, shared mechanics, and concrete style details.

## Triggers And Non-Triggers

| Type | Cues |
| --- | --- |
| Trigger | Design or restyle PPT decks, webpages, app screens, dashboards, UI components, frontend demos, templates, or static visual assets. |
| Trigger | Apply a named style such as `seu_design_style`, `renminbi_color_style`, or `chinese_traditional_color_style`. |
| Trigger | Add, validate, or update a concrete style inside this framework. |
| Non-trigger | Repository-level skill governance, renaming, registry policy, or cross-skill quality-gate design belongs to `meta-skill`. |
| Non-trigger | One-off bitmap image generation without reusable design-system translation belongs to an image generation workflow. |
| Ask if ambiguous | No concrete style can be resolved or multiple styles match equally. |

## Inputs And Outputs

| Contract | Details |
| --- | --- |
| Required inputs | Target artifact or design task, intended medium, content goal, and selected style or enough cues to resolve one. |
| Optional inputs | Audience/context, brand constraints, dimensions, source assets, accessibility requirements, output format, and platform constraints. |
| Normalized shape | `DesignRequest` with medium, content goal, audience/context, hard constraints, selected style, optional style modifiers, asset policy, and output requirements. |
| Outputs | Style-guided design specifications, PPT/UI/web/dashboard guidance, generated visual assets, implementation-ready code guidance, or concrete style updates. |
| Failure modes | Ask once before proceeding when style resolution is ambiguous, required assets are unsafe or missing, or a requested style extension would fork the shared workflow. |

## Workflow

1. Normalize the request into a `DesignRequest`:
   - medium: PPT/slides, web, app, dashboard, document visual, static visual, or design template.
   - goal: explain, persuade, compare, report, present, brand, sell, teach, or another explicit goal.
   - constraints: dimensions, platform, accessibility, required assets, output format, and brand requirements.
   - modifiers: optional user-requested palette, motif, texture, layout, mood, or asset adjustments that should be composed with the base style instead of treated as a new concrete style.
2. Resolve the concrete style:
   - load `references/style_registry.md` when listing styles, resolving aliases, or adding a style.
   - exact style name or alias wins; strong domain cue wins only when no style is explicit.
   - ask once if two styles match with similar confidence.
3. Load only the needed references:
   - for execution, load the selected `references/<style_name>.md` and only the shared reference needed by the task.
   - for style modifiers, load `references/style_modifier_contract.md`; use `references/design_mechanics.md` when modifiers affect palette, assets, or surface mechanics.
   - for validation or extension, load `references/style_contract.md`, `references/style_template.md`, and `references/design_mechanics.md` as needed.
4. Apply the invariant style pipeline:
   - normalize request;
   - resolve the base style;
   - extract requested modifiers from explicit modifier language, source assets, brand requirements, or constraints;
   - consume the concrete style through runtime concepts: style resolution, style identity, visual system, medium translation, resource policy, composition policy, and quality gate;
   - compose a `ComposedStylePlan` by blending compatible modifiers with the selected style's identity and medium needs; treat visible style-owned assets, user-provided files, shared providers, generated assets, and network materials as usable by default;
   - decide preview behavior from `previewMode` (`auto` by default): use explicit preview approval for ambiguous, high-stakes, public-facing, brand-sensitive, or user-requested preview work; otherwise create an internal `StyleLock` from style defaults and continue;
   - for multi-slide, multi-screen, long-page, or dense static outputs, create a `VisualRhythmPlan` before detailed composition: archetype sequence, per-surface visual anchors, motif/texture rotation, layout-density variation, and an `AssetUsePlan` that selects about 5-10 distinct asset roles or files for a normal deck/page; when the active style has few relevant visible files, fall back to downloading task-relevant assets from the network, generating vectors/bitmaps, or using shared providers rather than going asset-light;
   - when preview is needed, generate one style preview image or preview surface from the `StylePreviewPlan`, present its `StyleOptionSet[]`, and wait for user approval or replacement choices before full artifact generation;
   - when preview is not needed, record the locked defaults in `StyleLock` and disclose the important locked choices in the final note; when the user named no palette and no decisive content/brand cue forces one, choose the palette/series with `Default Series Selection` from `references/design_mechanics.md` (varied by default) instead of falling back to a single habitual card, and disclose it as an auto-varied default;
   - compose the artifact without style-specific branches in the base workflow and without silently changing locked palette, texture, layout density, visual rhythm, motif, or asset decisions;
   - run the concrete style self-check, variation checks from the visual rhythm plan, preview/lock consistency checks, and any modifier self-check rules, then revise only issues that materially affect usability or the requested style;
   - for non-wireframe visual artifacts, also produce an `AssetUseCheck` (see `references/style_contract.md`) as a delivery output covering asset count vs the 5-10 target, transparency/aspect-ratio/readability/relevance quality, and any rasterization done for unsupported vector formats; resolve its required fixes before delivery.
5. Enforce asset and surface boundaries:
   - inspect the active style's `assets/<style_name>/ASSET_MANIFEST.md` and visible files when building a real artifact; the framework docs stay inventory-opaque, but runtime generation must use the available asset boundary instead of assuming assets are absent.
   - visible assets inside the active style boundary, shared provider boundary, user-provided inputs, and network results are usable by default when their role fits the artifact; record their source/path and use role in task-local notes or the final QA note.
   - when a style's visible inventory is empty or thin for the needed role, download task-relevant assets from the network, generate vectors/bitmaps, or use shared providers; an empty `assets/<style_name>/` folder means "fetch assets at runtime", never "ship a shape-only artifact".
   - when the target medium cannot embed a vector asset (for example SVG in `python-pptx`), rasterize it via `cairosvg`, Inkscape, or `svglib` to RGBA `PNG`/`EMF` with the alpha channel preserved so transparent backgrounds stay transparent; treat unsupported formats as a conversion task, not a reason to drop the asset (see `references/design_mechanics.md`).
   - use another style's asset boundary as an additional hybrid source; note that choice in the final QA note.
   - preserve intrinsic aspect ratios for logos, wordmarks, motifs, and other informative assets whenever the active policy exports such assets.
   - apply shared texture providers when the active style declares a provider handle and fallback behavior; use visible provider assets when they improve the surface, and disable them only when they harm contrast or layout.
   - treat runtime assets, downloaded materials, generated bitmap/vector assets, user-provided assets, and code-native geometry as a prioritized mix: prefer semantically relevant assets and motifs for visual richness, use generated/code-native shapes for structure and diagrams, and use asset-off only when assets are materially harmful to readability or layout.
6. Deliver the artifact or code with a concise note of the style used and any assets used.

## Examples

Optional fixtures under `examples/` illustrate the workflow above; they do not add rules beyond `references/` and concrete style files. Load them only when learning the pipeline, maintaining the skill, or reproducing the sample deck — not on every design trigger.

| Need | Load |
| --- | --- |
| End-to-end deck built in `chinese_traditional_color_style`, with StyleLock, page sequence, and quality-gate notes | `examples/chinese_traditional_guide_deck/README.md` |
| Runnable PPT reference (python-pptx + Pillow + svglib) showing SVG→RGBA rasterization, the rice-paper provider texture, and an `AssetUseCheck` output | `examples/chinese_traditional_guide_deck/build_deck.py`, `examples/chinese_traditional_guide_deck/assets/`, and `examples/chinese_traditional_guide_deck/asset_use_check.json` |

Example copy uses **Intent**, **Creative Latitude**, and **Self-Check** language from style references. It does not ship extra imperative bans; style fidelity stays in the active `references/<style_name>.md` at delivery time.

## References

Load references progressively; do not read every reference by default.

| Need | Load |
| --- | --- |
| Resolve available styles, aliases, or priority | `references/style_registry.md` |
| Validate interfaces, data shapes, preview negotiation, asset policy, or self-check format | `references/style_contract.md` |
| Apply user-requested palette, motif, texture, layout, mood, or asset adjustments | `references/style_modifier_contract.md` |
| Add a new concrete style | `references/style_template.md` plus `references/style_contract.md` |
| Apply shared palette, preview surface, asset, or optional surface mechanics | `references/design_mechanics.md` |
| Apply SEU institutional academic style | `references/seu_design_style.md` |
| Apply RMB banknote-inspired style | `references/renminbi_color_style.md` |
| Apply Chinese traditional color style | `references/chinese_traditional_color_style.md` |

## Resources

| Resource | Role | Notes |
| --- | --- | --- |
| `references/style_registry.md` | concrete-style registry | Source of truth for style discovery and resolution metadata. |
| `references/style_contract.md` | formal contract | `DesignStyleBase` abstract class, implementation-class mapping, data-shape, visual-rhythm, asset-policy, surface-policy, and self-check definitions. |
| `references/style_modifier_contract.md` | modifier rules | Modifier extraction, compatibility, conflict handling, asset-source rules, and modifier self-check examples. |
| `references/style_template.md` | extension template | Skeleton for future concrete style implementations. |
| `references/design_mechanics.md` | shared mechanics | Reusable palette progression, visual-rhythm planning, style-owned asset interface, and active surface-provider rules. |
| `references/*_style.md` | concrete styles | Style-specific triggers, color, typography, layout, medium translation, opaque asset policy, and self-checks. |
| `assets/<style_name>/` | style-owned asset boundary | Required for every concrete style. User-editable runtime resources; an empty folder means "download/generate assets at runtime", never "ship without assets". File inventories stay inside `ASSET_MANIFEST.md`, not in framework references. |
| `scripts/validate_styles.py` | style validator | Static conformance check for registry entries, concrete style sections, required asset boundaries, asset handles, surface-policy shape, and runtime fallback metadata without inspecting bundled file inventories. |
| `examples/` | optional fixtures | Worked sample deck (`chinese_traditional_guide_deck/`): StyleLock notes, page sequence, and `build_deck.py` that rasterizes style-owned SVGs to RGBA, applies the rice-paper provider texture, and emits an `AssetUseCheck`. |

## Recommended Material Sources And Network Acquisition

Material discovery is a skill-level capability, not a concrete-style implementation detail. For runnable design work, use network discovery as an active design option when internet access is available: browse recommended sources for task-relevant materials, compare them with runtime assets, generated vectors, code-native geometry, and user-provided assets, then use the option that best preserves the selected style while reducing monotony. Do this even when runtime assets are available, unless the user forbids browsing, the environment is offline, or the current artifact clearly needs no external visual material. Use visible assets freely; this is a personal-use skill, so do not gate assets behind brand, copyright, or commercial-rights checks.

| Source | Best for | Integration rule |
| --- | --- | --- |
| Pixabay (`https://pixabay.com/`) | photos, illustrations, vectors, videos, music, sound effects, 3D models, GIFs, and broad visual reference material | Use as the primary international stock-media source. Record the item URL and role when convenient so assets can be re-found. |
| Iconfont / 阿里巴巴矢量图标库 (`https://www.iconfont.cn/`) | Chinese icon sets, SVG symbols, UI icons, pictograms, and iconfont workflows | Use as the primary China-local icon/vector source. Record the item or project URL when convenient so assets can be re-found. |

Acquisition rules:

- Search and compare task-relevant materials for design fit, rhythm, and semantic value; download candidates when they improve the artifact.
- For a normal multi-slide deck, website, app mockup, dashboard, or static visual, target about 5-10 distinct visual assets or asset roles across the artifact. Count style-owned SVGs, texture wrappers, sourced images/icons, generated bitmap/vector assets, and user-provided files; do not count plain rectangles, lines, text boxes, or routine chart shapes.
- A zero-media or shape-only artifact is acceptable only when the user explicitly asks for it or the output is a pure wireframe/data diagram. When a style's visible inventory is empty or thin, download or generate assets rather than shipping shape-only output.
- Keep imported reusable files inside the standard `assets/<style_name>/` boundary rather than source-specific subdirectories such as `assets/<style_name>/<source_name>/`.
- When useful, note a downloaded asset's source URL and intended role so it can be re-found later. Detailed provenance bookkeeping is optional for this personal-use skill.

Concrete styles may opt in to texture providers through `SurfaceTexturePolicy` handles, declared fallback behavior, and token lists; framework validation leaves provider internals under `assets/` opaque. For new external acquisition, use Pixabay and Iconfont unless the skill-level source table is intentionally updated later. External sources should support style identity, asset boundaries, and readability.

## Extension

To add or update a concrete style:

1. Create or edit `references/<style_name>.md` from `references/style_template.md`.
2. Register the style in `references/style_registry.md` with aliases, domain cues, medium cues, priority, and asset root.
3. Implement `DesignStyleBase` from `references/style_contract.md` and include a concise `Contract Conformance` section near the top of the style file.
4. Keep style-specific decisions inside the concrete style file; keep shared mechanics in `references/design_mechanics.md`.
5. Create `assets/<style_name>/` and `assets/<style_name>/ASSET_MANIFEST.md` for every concrete style. The folder may start empty; an empty boundary means assets are fetched or generated at runtime, not that the artifact ships without assets. Keep reusable files inside that boundary and expose only stable policy handles and runtime fallback rules from skill documents.
6. Run the quality gates before delivery.

## Design Invariants

- Style is structure plus behavior, not only colors.
- Concrete styles must be substitutable through the same dispatch workflow.
- Shared mechanics must stay reusable and style-neutral.
- Semantic roles and readability guide decorative preference without narrowing creative exploration.
- Asset-rich output is the default for visual artifacts: use visible style assets, texture providers, sourced materials, generated assets, and user-provided files to create visual range. When a style's visible inventory is empty or thin, download or generate assets; shape-only output is reserved for explicit wireframe/data-diagram requests.
- Asset use is governed by purpose, not volume: every asset earns its place through a semantic or structural role, and the richness range guides coverage rather than imposing a quota. Drop assets that duplicate an existing anchor, fight the visual hierarchy, weaken contrast or legibility, burden load, or decorate without meaning — asset-rich is never asset-cluttered.
- Multi-page visual rhythm uses planned anchors, archetype variation, motif rotation, and variation checks to create range without forcing a single conservative look.
- Identity and motif assets require proportion-preserving placement.
- Asset availability is resolved at runtime through `AssetPolicy` plus inspection of visible files in the selected asset boundary; every concrete style provides a network/generation fallback and a required `assets/<style_name>/` boundary with `ASSET_MANIFEST.md`. An empty boundary triggers network download or generation.
- New styles extend the framework; they do not fork the base workflow.

## Quality Gate

Before delivery or commit:

- Run `python skills/my-design-style/scripts/validate_styles.py` for style-family conformance.
- Run `python skills/meta-skill/scripts/validate_skills.py` for repository-level skill structure.
- Run `git diff --check` for whitespace and conflict markers.
- Manually verify visual outputs for alignment, spacing, hierarchy, text overflow, contrast, responsiveness, visual-anchor coverage, archetype variation, motif rotation, image distortion, decorative relevance, asset count/range, and style fidelity.
- Produce and pass an `AssetUseCheck` for non-wireframe visual artifacts: confirm the distinct-asset count is in the 5-10 guide range (a guide, not a hard quota; a restrained style may sit at the low end when each asset earns a role, and a thin inventory should be filled by downloading or generating assets rather than padding), available style-owned/provider/sourced/generated assets were used instead of an all-code-native shortcut, vector assets the medium cannot embed were rasterized to RGBA with transparency preserved (no white/opaque box on colored or textured surfaces), and every asset earns a role without harming aspect ratio, contrast, or readability.
