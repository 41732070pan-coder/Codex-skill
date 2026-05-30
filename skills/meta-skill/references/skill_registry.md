# Skill Registry

This registry is the repository-level inventory for maintained skills. Keep it concise; detailed behavior belongs in each skill directory.

| Skill | Path | Type | Status | Function | Trigger cues | Primary outputs | Overlap risks | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `meta-skill` | `skills/meta-skill/` | meta | stable | Designs, reviews, renames, refactors, and governs repository skills and implementation families. | New skill, skill rename, skill audit, implementation family, loading boundary, governance contract, registry, template, validator. | Skill plans, contracts, templates, registries, loading-boundary audits, validators. | Concrete domain execution without structural or governance changes. | Stable foundation. |
| `my-design-style` | `skills/my-design-style/` | domain | experimental | Applies extensible visual styles to PPT, web, app, dashboard, and static visual work. | PPT style, web visual style, app/dashboard visual system, SEU/RMB/traditional Chinese color style. | Style-guided designs, UI/PPT specifications, visual assets or code guidance. | Repository skill governance belongs to `meta-skill`; generic image generation belongs elsewhere. | Usable and still evolving. |
| `tutorial-learning` | `skills/tutorial-learning/` | workflow | experimental | Converts PDF, HTML, Markdown, and web tutorial sources into medium-neutral, source-traced Chinese course-design bundles. | PDF textbook, HTML tutorial, Markdown guide, web tutorial, chapter study, section lecture, triage, micro-assessment, review cards. | Learning plans, Chinese lecture markdown, tutorial structures, source-traced triage, assessments, practice, review plans, and fidelity evidence. | Raw PDF rendering and OCR belong to document tooling; HTML, PPT, H5, DOCX, visual style, and runtime persistence belong to downstream renderers. | Instructional-design intermediate layer only. |

## Entry Shape

```ts
interface SkillRegistryEntry {
  skillName: string;
  path: `skills/${string}/`;
  type: "meta" | "domain" | "tool" | "workflow";
  status: "draft" | "experimental" | "stable" | "deprecated";
  function: string;
  triggerCues: string[];
  primaryOutputs: string[];
  overlapRisks: string[];
  notes?: string;
}
```

## Registry Rules

- Add one row whenever a maintained skill is added, renamed, deprecated, or removed.
- Keep the root README skill table aligned with this registry, but shorter. Status values must use the `SkillRegistryEntry.status` enum; put display wording in `notes` instead of overloading `status`.
- Keep table columns aligned with `SkillRegistryEntry`; do not hide trigger cues or overlap risks only in prose.
- Do not put detailed internal strategy lists here unless they affect repository-level discovery.
