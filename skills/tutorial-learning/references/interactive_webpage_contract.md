# Interactive Tutorial Webpage Contract

The final learner-facing deliverable is a runnable, content-first `interactive_tutorial.html`. It is not a webpage design memo. The page should help the learner understand and practice the routed tutorial content without requiring them to open audit JSON files or reconstruct a UI from Markdown instructions.

## Product Priority

Use this order when tradeoffs arise:

1. Preserve source fidelity and the requested tutorial boundary.
2. Teach the selected core and supporting content clearly in Chinese.
3. Make learning active with prediction, teach-back, application, practice, and review interactions.
4. Keep the learner oriented with a study plan, progress state, and homepage navigation.
5. Add visual polish only after the learning flow works.

Do not spend most of the output on design-system prose, generic layouts, or implementation commentary. The rendered page must contain the actual lesson content.

## Delivery Order And Scope

1. Emit `learning_plan.md` first so the learner can see the full learning arrangement.
2. Estimate routed lesson count and study minutes.
3. Choose one delivery mode:
   - `complete_course`: use when the routed course is small enough to render coherently in one pass (default guideline: at most 3 lesson pages and at most 90 estimated study minutes).
   - `progressive_chapter`: use for longer sources. Render the homepage, complete plan, and first useful chapter or section now. Keep later lessons visible as `planned` homepage-navigation items and render them as the learner progresses.
4. Emit runnable `interactive_tutorial.html` with embedded or linked CSS and JavaScript. Prefer a self-contained HTML file for portable delivery unless the user asks for a framework project.

## Required Learning Plan

`learning_plan.md` keeps this compact structure:

```markdown
# 学习计划
## 学习范围与目标
## 内容规模判断
- 预计总时长：...
- 预计课程页：...
- 交付模式：complete_course | progressive_chapter
- 判断理由：...
## 学习阶段安排
| 阶段 | 页面或章节 | 学习目标 | 预计分钟 | 状态 | 解锁条件 |
| --- | --- | --- | ---: | --- | --- |
## 本轮生成范围
## 后续生成规则
## 复习节奏
```

Use `ready`, `current`, `planned`, and `completed` as states.

## Required Interactive HTML Shape

Use semantic HTML and stable hooks so the output is usable and auditable:

```html
<body data-delivery-mode="complete_course|progressive_chapter">
  <header>...</header>
  <nav id="home-nav" aria-label="学习导航">...</nav>
  <main>
    <section id="learning-plan">...</section>
    <article class="lesson-page" data-page-state="current">...</article>
    <section id="review-center">...</section>
  </main>
  <script>...</script>
</body>
```

The page must include:

- homepage navigation with the learning plan, each current/ready lesson, planned future lessons when applicable, and review center;
- lesson objectives, estimated time, source-boundary disclosure, actual Chinese explanation content, and useful source identifiers;
- prediction, teach-back, and application micro-test controls when applicable;
- a small practice task and a completion action;
- review-card entry point and spaced-review reminder;
- responsive layout and accessible labels, focus behavior, and non-color-only state expression.

## Content Rules

- Render explanation content from the lecture route. Do not replace teaching with cards that only say “see lecture.md”.
- Preserve commands, API names, formulas, identifiers, and URLs in source spelling.
- Keep filler out of the lesson body. Put useful reference-only material in a secondary appendix or disclosure.
- Keep source traces visible but secondary: learners need trust without having audit metadata dominate the explanation.
- In progressive mode, the current lesson must be complete enough to study now. Planned lessons may show titles, goals, and unlock conditions but must not pretend their teaching content has already been generated.

## Minimum Interactions

Implement usable client-side behavior, not static labels:

- switch between homepage, plan, lesson, and review views;
- reveal or check micro-test feedback after a learner action;
- mark the current lesson complete and update progress state;
- reveal review-card hints or answers;
- preserve current progress locally when practical, for example with `localStorage`.

## Optional Design Notes

Generate a separate `webpage_design.md` only when the user explicitly asks for a design handoff. It may explain visual decisions, but it never replaces `interactive_tutorial.html` and should remain shorter than the learning content.

## Quality Gate

Before delivery verify:

- `learning_plan.md` exists and the HTML mode matches its delivery mode;
- the HTML page contains substantial tutorial explanation, not only navigation or design placeholders;
- the homepage navigation includes plan, lesson, review, and progressive planned entries when required;
- the current lesson contains objectives, content, micro-test, practice, completion, and review affordances;
- JavaScript wires navigation, feedback reveal/checking, completion, and review-card interaction;
- audit sidecars remain secondary to the learner-facing tutorial experience.
