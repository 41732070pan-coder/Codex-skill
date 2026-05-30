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
   - `progressive_chapter`: use for longer sources. Render the homepage, complete route, and one complete useful lesson now. Follow `progressive_generation_contract.md`: distinguish `current`, `ready-to-generate`, `locked`, and `completed`; keep future lessons inspectable; and let the learner explicitly click `生成并开始下一课` when ready.
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

Use `completed`, `current`, `ready-to-generate`, and `locked` as progressive lesson states. For a small `complete_course`, every generated lesson may be `current` or `completed`.

## Required Interactive HTML Shape

Use semantic HTML and stable hooks so the output is usable and auditable:

```html
<body data-delivery-mode="complete_course|progressive_chapter" data-design-skill="my-design-style" data-theme="chinese-traditional-color-style">
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

- homepage navigation with the learning plan, each current lesson, inspectable `ready-to-generate` and `locked` future route item when applicable, completed lessons, and review center;
- lesson objectives, estimated time, source-boundary disclosure, actual Chinese explanation content, and useful source identifiers;
- prediction, teach-back, and application micro-test controls when applicable; require input before revealing feedback;
- a small practice task, self-check criteria, and a completion action;
- for progressive tutorials, a visible explanation-preference selector and `生成并开始下一课` action after completion;
- centralized theme tokens resolved through `design_style_interface.md`, defaulting to `my-design-style` / `chinese-traditional-color-style`;
- review-card entry point and spaced-review reminder;
- responsive layout and accessible labels, focus behavior, and non-color-only state expression.

## Content Rules

- Render explanation content from the lecture route. Do not replace teaching with cards that only say “see lecture.md”.
- Preserve commands, API names, formulas, identifiers, and URLs in source spelling.
- Keep filler out of the lesson body. Put useful reference-only material in a secondary appendix or disclosure.
- Keep source traces visible but secondary: learners need trust without having audit metadata dominate the explanation.
- In progressive mode, the current lesson must be a complete study unit. Future lessons may show route-level titles, lightweight previews, and unlock conditions but must not pretend their teaching content has already been generated. Locked previews explain why they are locked instead of acting as silent disabled controls.
- Include scenario, intuition, definitions, positive example, counterexample, misconceptions, practice analysis, recap, and next-lesson bridge when the generated lesson calls for them.
- Show dynamic time estimates for reading, assessment, practice, and recap rather than forcing a fixed lesson duration.

## Minimum Interactions

Implement usable client-side behavior, not static labels:

- switch between homepage, plan, lesson, and review views;
- reveal or check micro-test feedback only after a learner attempt; preserve attempts, repeated errors, and uncertain-topic signals locally;
- mark the current lesson complete after core reading, required assessment attempts, practice submission, and explicit learner confirmation; do not require every answer to be correct;
- in progressive mode, preview locked route items and explicitly generate the next lesson after learner action;
- reveal review-card hints or answers;
- mirror current progress to `localStorage` for responsive UI when practical, and persist or export learner submissions and confirmations using `learner_state_contract.md`;
- provide visible `下载学习记录` and `导出下一课上下文` actions in portable static HTML so local JSON can be attached to a later model run.

## Learner-State Persistence

Follow `learner_state_contract.md`. Generated course artifacts include `state/learner_state.json` and `state/next_lesson_context.json`. A filesystem-capable runtime updates them atomically. Portable static HTML must expose `exportLearnerState()` and `buildNextLessonContext()` through visible export actions because browser `localStorage` cannot silently write arbitrary local files. Before next-lesson generation, rebuild compact context from durable learner state; do not ask a model to scrape rendered HTML or raw browser storage.

## Visual Style Interface

Apply `design_style_interface.md`. Keep style resolution centralized in CSS custom properties or an equivalent token layer. Unless the learner overrides it, use `my-design-style` with `chinese-traditional-color-style` and a restrained academy-like variant. Preserve semantic HTML, keyboard focus, readable contrast, and text labels for every state. A theme may change presentation but never remove learning interactions or obscure content.

## Optional Design Notes

Generate a separate `webpage_design.md` only when the user explicitly asks for a design handoff. It may explain visual decisions, but it never replaces `interactive_tutorial.html` and should remain shorter than the learning content.

## Quality Gate

Before delivery verify:

- `learning_plan.md` exists and the HTML mode matches its delivery mode;
- the HTML page contains substantial tutorial explanation, not only navigation or design placeholders;
- the homepage navigation includes plan, lesson, review, and inspectable progressive route entries when required;
- the current lesson contains objectives, full learning-unit content, attempt-first micro-test, practice, completion, and review affordances;
- progressive pages expose lock reasons, an explanation-preference selector, and explicit next-lesson generation;
- learner submissions and confirmations persist to local JSON files, and portable static pages visibly export both durable state and compact next-lesson context;
- visual styling is resolved through the interface and defaults to the Chinese traditional theme when no override exists;
- JavaScript wires navigation, attempt-first feedback, completion, next-generation state, and review-card interaction;
- audit sidecars remain secondary to the learner-facing tutorial experience.
