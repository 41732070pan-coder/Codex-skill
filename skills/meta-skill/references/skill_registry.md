# Skill Registry

This registry is the repository-level inventory for maintained skills. Keep it concise; detailed behavior belongs in each skill directory.

| Skill | Path | Type | Status | Function | Trigger cues | Primary outputs | Overlap risks | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `meta-skill` | `skills/meta-skill/` | meta | stable | Designs, reviews, renames, refactors, and governs repository skills and implementation families. | New skill, skill rename, skill audit, implementation family, loading boundary, governance contract, registry, template, validator. | Skill plans, contracts, templates, registries, loading-boundary audits, validators. | Concrete domain execution without structural or governance changes. | Stable foundation. |
| `my-design-style` | `skills/my-design-style/` | domain | experimental | Applies extensible visual styles to PPT, web, app, dashboard, and static visual work. | PPT style, web visual style, app/dashboard visual system, SEU/RMB/traditional Chinese color style. | Style-guided designs, UI/PPT specifications, visual assets or code guidance. | Repository skill governance belongs to `meta-skill`; generic image generation belongs elsewhere. | Usable and still evolving. |
| `professional-tutorial-learning` | `skills/professional-tutorial-learning/` | workflow | experimental | Converts professional tutorials from PDF, web, video, transcript, or mixed sources into focused learning and review artifacts. | Learn tutorial, PDF course, web tutorial, video transcript, lesson notes, study plan, checkpoints, review prompts. | Markdown lessons, knowledge-point maps, skip/read classifications, practice tasks, checkpoints, review schedules, iteration logs. | Repository skill governance belongs to `meta-skill`; visual styling belongs to `my-design-style`; generic summarization without learning workflow may not need a skill. | Markdown-first and web-app-ready. |

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
