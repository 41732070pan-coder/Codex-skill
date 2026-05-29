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
| Ask if ambiguous | No concrete style can be resolved, multiple styles match equally, or requested assets lack provenance or safe usage rules. |

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
   - compose a `ComposedStylePlan` only when modifiers satisfy the selected style's composition policy and base invariants; downgrade or reject conflicting modifiers instead of silently replacing the base style;
   - decide preview behavior from `previewMode` (`auto` by default): use explicit preview approval for ambiguous, high-stakes, public-facing, brand-sensitive, or user-requested preview work; otherwise create an internal `StyleLock` from style defaults and continue;
   - for multi-slide, multi-screen, long-page, or dense static outputs, create a `VisualRhythmPlan` before detailed composition: archetype sequence, per-surface visual anchors, motif/texture rotation, layout-density variation, and asset fallback choices;
   - when preview is needed, generate one style preview image or preview surface from the `StylePreviewPlan`, present its `StyleOptionSet[]`, and wait for user approval or replacement choices before full artifact generation;
   - when preview is not needed, record the locked defaults in `StyleLock` and disclose the important locked choices in the final note;
   - compose the artifact without style-specific branches in the base workflow and without silently changing locked palette, texture, layout density, visual rhythm, motif, or asset decisions;
   - run the concrete style self-check, anti-monotony checks from the visual rhythm plan, preview/lock consistency checks, and any modifier self-check rules, then revise until they pass.
5. Enforce asset and surface boundaries:
   - use only the active style's declared assets and manifest.
   - never browse `assets/` for arbitrary ornament.
   - preserve intrinsic aspect ratios for logos, wordmarks, motifs, and other informative assets.
   - do not apply shared texture providers unless the active style declares an available provider and all referenced provider files exist.
   - when style-owned assets are unavailable or inappropriate, use the active style's declared code-native geometry, diagram, swatch, typography, rule, or user-provided-asset fallback instead of leaving pages visually empty.
6. Deliver the artifact or code with a concise note of the style used, any assets used, and any unresolved constraints.

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
| `references/*_style.md` | concrete styles | Style-specific triggers, color, typography, layout, medium translation, assets, and self-checks. |
| `assets/seu_design_style/` | SEU style-owned assets | Official SEU SVG identity/motif assets; use only through `seu_design_style` asset policy and manifest. |
| `assets/renminbi_color_style/` | reserved empty asset folder | Currently contains no bundled files; `renminbi_color_style` uses code-native geometry, generated vectors, user-provided assets, or approved Pixabay/Iconfont project assets. |
| `assets/chinese_traditional_color_style/` | reserved empty asset folder | Currently contains no bundled files; `chinese_traditional_color_style` uses named colors, code-native geometry, generated vectors, user-provided assets, or approved Pixabay/Iconfont project assets. |
| `assets/transparent_textures/` | shared surface provider | Curated Transparent Textures SVG wrappers, manifest, JSON index, provenance, and checksums for concrete style opt-in. |
| `scripts/validate_styles.py` | style validator | Static conformance check for registry entries, concrete style sections, declared assets, and unavailable provider references. |

## Recommended Material Sources And Network Acquisition

Material discovery is a skill-level capability, not a concrete-style implementation detail. When a runnable design task needs assets that are not already bundled and internet access is available, the agent may browse recommended sources, download task-relevant materials, and record provenance before use. Keep this source list extensible; future sources should be added here rather than hard-coded into individual style files.

| Source | Best for | Integration rule |
| --- | --- | --- |
| Pixabay (`https://pixabay.com/`) | photos, illustrations, vectors, videos, music, sound effects, 3D models, GIFs, and broad visual reference material | Use as the primary international stock-media source. Check the Pixabay Content License for each asset and record the item URL, creator when visible, license/usage note, download date, file type, dimensions when known, SHA-256, role, and safe placement. Do not use content as standalone resale material, trademarks/logos/brands for commercial goods, misleading endorsement, or trademark/service-mark material. |
| Iconfont / 阿里巴巴矢量图标库 (`https://www.iconfont.cn/`) | Chinese icon sets, SVG symbols, UI icons, pictograms, and iconfont workflows | Use as the primary China-local icon/vector source. Check the icon or collection page for author/copyright/commercial-use notes before use. Record item or project URL, author/source when visible, license or permission note, download date, file type, SHA-256, role, and safe placement. For commercial use or unclear rights, obtain permission or ask the user to provide a licensed file. |

Acquisition rules:

- Download only materials that are needed for the current task or an explicit skill-asset extension; do not download decorative filler.
- Do not create source-specific subdirectories such as `assets/<style_name>/<source_name>/`; `assets/<style_name>/` is the standard style asset boundary.
- Before using a downloaded asset, record source URL, source name, download date, file type, dimensions when known, size, SHA-256, intended role, safe placement, and license/usage notes in the relevant manifest or project documentation.
- Prefer no-login, no-paywall sources. Do not bypass login, VIP, paywall, watermark, rate-limit, robots/access-control, API-key-only, or licensing flows; if rights are unclear, use the material only as a reference or ask the user to provide a licensed file.
- Public, commercial, brand-sensitive, identity-sensitive, financial, legal/security-document-adjacent, people/trademark/logo/brand-containing, or photo-based work requires explicit rights and safety review before downloaded third-party files become final production assets.

Concrete styles may opt in to bundled textures only through explicit `SurfaceTexturePolicy` tokens that exist in `texture_index.json`, preserve provenance, and pass `scripts/validate_styles.py`. For new external acquisition, use only Pixabay and Iconfont unless the skill-level source table is intentionally updated later. External sources never override style anti-goals, asset boundaries, readability, or provenance requirements.

## Extension

To add or update a concrete style:

1. Create or edit `references/<style_name>.md` from `references/style_template.md`.
2. Register the style in `references/style_registry.md` with aliases, domain cues, medium cues, priority, and asset root.
3. Implement `DesignStyleBase` from `references/style_contract.md` and include a concise `Contract Conformance` section near the top of the style file.
4. Keep style-specific decisions inside the concrete style file; keep shared mechanics in `references/design_mechanics.md`.
5. Add style-owned assets only under `assets/<style_name>/`, include an `ASSET_MANIFEST.md`, and document provenance, discovery source, search keywords, allowed/forbidden use, and whether the asset is directly sourced, traced, generated, or code-authored.
6. Run the quality gates before delivery.

## Design Invariants

- Style is structure plus behavior, not only colors.
- Concrete styles must be substitutable through the same dispatch workflow.
- Shared mechanics must stay reusable and style-neutral.
- Semantic roles and readability beat decorative preference.
- Multi-page visual rhythm requires planned anchors, archetype variation, motif rotation, and anti-monotony checks.
- Identity and motif assets require proportion-preserving placement.
- A style with no bundled assets must explicitly declare `assetRoot: none` and a fallback policy.
- New styles extend the framework; they do not fork the base workflow.

## Quality Gate

Before delivery or commit:

- Run `python skills/my-design-style/scripts/validate_styles.py` for style-family conformance.
- Run `python skills/meta-skill/scripts/validate_skills.py` for repository-level skill structure.
- Run `git diff --check` for whitespace and conflict markers.
- Manually verify visual outputs for alignment, spacing, hierarchy, text overflow, contrast, responsiveness, visual-anchor coverage, archetype variation, motif rotation, image distortion, decorative relevance, asset provenance, and style fidelity.
