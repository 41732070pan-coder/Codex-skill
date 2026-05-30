# Design Style Interface

Keep tutorial pedagogy and visual styling separate. The tutorial-learning skill owns information architecture, lesson content, learning state, assessments, and review behavior. A design-style provider owns visual tokens and component presentation without changing those learning invariants.

## Default Provider

When the user does not request another visual direction, use:

```json
{
  "designSkill": "my-design-style",
  "theme": "chinese-traditional-color-style",
  "themeVariant": "academy-calm"
}
```

Load `../../my-design-style/SKILL.md` and `../../my-design-style/references/chinese_traditional_color_style.md` when applying this default. Prefer a restrained Chinese traditional academy atmosphere: readable long-form text, ink-like contrast, paper-like surfaces, measured whitespace, and sparse ornamental accents. Do not let decoration reduce usability.

## Input Shape

```ts
interface TutorialDesignStyleRequest {
  designSkill?: string; // default "my-design-style"
  theme?: string; // default "chinese-traditional-color-style"
  themeVariant?: string; // default "academy-calm"
  customOverrides?: {
    colors?: Record<string, string>;
    fonts?: Record<string, string>;
    spacingScale?: string;
    illustrationDensity?: "none" | "low" | "medium";
    motionIntensity?: "none" | "low" | "medium";
  };
}
```

## Provider Output Contract

A style provider should resolve:

1. color tokens for background, text, accent, border, success, warning, locked, and focus states;
2. title, body, annotation, quote, and navigation typography;
3. spacing, radius, elevation, and border treatment;
4. styles for navigation, progress, buttons, cards, assessment feedback, review cards, and locked previews;
5. illustration and ornament guidance;
6. responsive behavior;
7. accessibility requirements, including keyboard focus and non-color-only state expression.

## Required Boundaries

- Preserve semantic HTML, stable JavaScript hooks, and learner-facing state labels across themes.
- Do not scatter theme-specific values through lesson content templates. Resolve provider tokens into CSS custom properties or an equivalent centralized layer.
- Treat lock, success, warning, and current states as text-and-shape distinctions, not color-only distinctions.
- Keep body copy readable for long study sessions. Ornament is secondary to comprehension.
- If the named provider is unavailable, use a readable neutral fallback and state that fallback explicitly.
