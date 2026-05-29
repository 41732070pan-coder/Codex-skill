# Skill Registry

This registry is the repository-level inventory for maintained skills. Keep it concise; detailed behavior belongs in each skill directory.

| Skill | Path | Type | Status | Function | Primary outputs |
| --- | --- | --- | --- | --- | --- |
| `meta-skill` | `skills/meta-skill/` | Meta / governance | Stable foundation | Designs, reviews, renames, refactors, and governs repository skills. | Skill plans, contracts, templates, registries, audits. |
| `my-design-style` | `skills/my-design-style/` | Domain / design system | Usable | Applies extensible visual styles to PPT, web, app, dashboard, and static visual work. | Style-guided designs, UI/PPT specifications, visual assets or code guidance. |

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
}
```

## Registry Rules

- Add one row whenever a maintained skill is added, renamed, deprecated, or removed.
- Keep the root README skill table aligned with this registry, but shorter.
- Do not put detailed internal strategy lists here unless they affect repository-level discovery.
