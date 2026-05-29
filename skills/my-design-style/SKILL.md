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
| Normalized shape | `DesignRequest` with medium, content goal, audience/context, hard constraints, selected style, asset policy, and output requirements. |
| Outputs | Style-guided design specifications, PPT/UI/web/dashboard guidance, generated visual assets, implementation-ready code guidance, or concrete style updates. |
| Failure modes | Ask once before proceeding when style resolution is ambiguous, required assets are unsafe or missing, or a requested style extension would fork the shared workflow. |

## Workflow

1. Normalize the request into a `DesignRequest`:
   - medium: PPT/slides, web, app, dashboard, document visual, static visual, or design template.
   - goal: explain, persuade, compare, report, present, brand, sell, teach, or another explicit goal.
   - constraints: dimensions, platform, accessibility, required assets, output format, and brand requirements.
2. Resolve the concrete style:
   - load `references/style_registry.md` when listing styles, resolving aliases, or adding a style.
   - exact style name or alias wins; strong domain cue wins only when no style is explicit.
   - ask once if two styles match with similar confidence.
3. Load only the needed references:
   - for execution, load the selected `references/<style_name>.md` and only the shared reference needed by the task.
   - for validation or extension, load `references/style_contract.md`, `references/style_template.md`, and `references/design_mechanics.md` as needed.
4. Apply the invariant style pipeline:
   - normalize request;
   - resolve style;
   - consume the concrete style as a `DesignStyleBase` implementation (`resolve`, `getIntent`, `getPalette`, `getTypography`, `getLayoutSystem`, `getMediumTranslation`, `getAssetPolicy`, `getSurfaceTexturePolicy`, `selfCheck`);
   - compose the artifact without style-specific branches in the base workflow;
   - run the concrete style self-check and revise until it passes.
5. Enforce asset and surface boundaries:
   - use only the active style's declared assets and manifest.
   - never browse `assets/` for arbitrary ornament.
   - preserve intrinsic aspect ratios for logos, wordmarks, motifs, and other informative assets.
   - do not apply shared texture providers unless the active style declares an available provider and all referenced provider files exist.
6. Deliver the artifact or code with a concise note of the style used, any assets used, and any unresolved constraints.

## References

Load references progressively; do not read every reference by default.

| Need | Load |
| --- | --- |
| Resolve available styles, aliases, or priority | `references/style_registry.md` |
| Validate interfaces, data shapes, asset policy, or self-check format | `references/style_contract.md` |
| Add a new concrete style | `references/style_template.md` plus `references/style_contract.md` |
| Apply shared palette, asset, or optional surface mechanics | `references/design_mechanics.md` |
| Apply SEU institutional academic style | `references/seu_design_style.md` |
| Apply RMB banknote-inspired style | `references/renminbi_color_style.md` |
| Apply Chinese traditional color style | `references/chinese_traditional_color_style.md` |

## Resources

| Resource | Role | Notes |
| --- | --- | --- |
| `references/style_registry.md` | concrete-style registry | Source of truth for style discovery and resolution metadata. |
| `references/style_contract.md` | formal contract | `DesignStyleBase` abstract class, implementation-class mapping, data-shape, asset-policy, surface-policy, and self-check definitions. |
| `references/style_template.md` | extension template | Skeleton for future concrete style implementations. |
| `references/design_mechanics.md` | shared mechanics | Reusable palette progression, style-owned asset interface, and inactive surface-provider extension rules. |
| `references/*_style.md` | concrete styles | Style-specific triggers, color, typography, layout, medium translation, assets, and self-checks. |
| `assets/seu_design_style/` | SEU style-owned assets | Official SEU SVG identity/motif assets; use only through `seu_design_style` asset policy and manifest. |
| `scripts/validate_styles.py` | style validator | Static conformance check for registry entries, concrete style sections, declared assets, and unavailable provider references. |

The canonical shared texture provider source is Transparent Textures (`https://www.transparenttextures.com/`). No shared texture asset provider is currently bundled; before any concrete style can enable `transparent_textures`, selected files must be added with a manifest, index, provenance, and explicit style opt-in.

## Extension

To add or update a concrete style:

1. Create or edit `references/<style_name>.md` from `references/style_template.md`.
2. Register the style in `references/style_registry.md` with aliases, domain cues, medium cues, priority, and asset root.
3. Implement `DesignStyleBase` from `references/style_contract.md` and include an `Implementation Map` near the top of the style file.
4. Keep style-specific decisions inside the concrete style file; keep shared mechanics in `references/design_mechanics.md`.
5. Add style-owned assets only under `assets/<style_name>/`, include an `ASSET_MANIFEST.md`, and document provenance and allowed/forbidden use.
6. Run the quality gates before delivery.

## Design Invariants

- Style is structure plus behavior, not only colors.
- Concrete styles must be substitutable through the same dispatch workflow.
- Shared mechanics must stay reusable and style-neutral.
- Semantic roles and readability beat decorative preference.
- Identity and motif assets require proportion-preserving placement.
- A style with no bundled assets must explicitly declare `assetRoot: none` and a fallback policy.
- New styles extend the framework; they do not fork the base workflow.

## Quality Gate

Before delivery or commit:

- Run `python skills/my-design-style/scripts/validate_styles.py` for style-family conformance.
- Run `python skills/meta-skill/scripts/validate_skills.py` for repository-level skill structure.
- Run `git diff --check` for whitespace and conflict markers.
- Manually verify visual outputs for alignment, spacing, hierarchy, text overflow, contrast, responsiveness, image distortion, decorative relevance, asset provenance, and style fidelity.
