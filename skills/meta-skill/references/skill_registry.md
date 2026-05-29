# Skill Registry

This registry is the repository-level inventory for maintained skills. Keep it concise; detailed behavior belongs in each skill directory.

| Skill | Path | Type | Status | Function | Primary outputs | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `meta-skill` | `skills/meta-skill/` | Meta / governance | stable | Designs, reviews, renames, refactors, and governs repository skills. | Skill plans, contracts, templates, registries, audits. | Stable foundation. |
| `my-design-style` | `skills/my-design-style/` | Domain / design system | experimental | Applies extensible visual styles to PPT, web, app, dashboard, and static visual work. | Style-guided designs, UI/PPT specifications, visual assets or code guidance. | Usable and still evolving. |

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
- Do not put detailed internal strategy lists here unless they affect repository-level discovery.
