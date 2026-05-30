# Lecture Template (Chinese)

Use this shape for each tutorial section lecture. YAML front matter and every level-two section below are required. When a conditional section does not apply, keep the heading and state that it is not applicable.

```yaml
---
skill: tutorial-learning
source_format: pdf|html|markdown|plain_text_with_headings
source_title: "<title>"
source_locator: "<url or path>"
section_id: "<stable section id>"
section_title: "<Chinese section title>"
est_minutes_total: <number>
learning_objectives:
  - id: lo1
    text: "<Chinese objective>"
    mastery: exposure|recall|application
    verifiable: "<how to verify>"
    source_trace_ids: [st1]
triage_summary:
  core_blocks: <n>
  skipped_blocks: <n>
  appendix_blocks: <n>
---
```

## 本节目标

2–4 bullets tied to `learning_objectives`. Each objective must be observable and source-traced.

## 来源与边界

Short table: source trace id | locator/page/anchor/heading | boundary confidence | evidence type.

## 学习路线

**Required.** Short table: block title | 角色 | 深度 | 预计分钟 | 说明.

Column `深度` must use: skip | skim | standard | deep.

## 核心讲解

Render every lesson as an independently studyable unit. Use ordered subsections for `core` and in-lecture `supporting` blocks:

1. **问题场景**：explain the learner-facing problem.
2. **直觉解释**：build an initial mental model.
3. **必要定义**：introduce terms, formulas, or boundaries.
4. **完整正例**：walk through one useful application.
5. **反例或失败案例**：show a plausible but wrong approach.
6. **常见误区**：name at least two misconceptions.
7. **下一课桥接**：explain how this concept will be reused.

- Teach mechanism, not source paste.
- Use Chinese; keep API names, commands, formulas, identifiers, and URLs in original spelling.
- For `skim` blocks: ≤ 1 short paragraph.
- Include source trace ids for major claims when useful.
- Estimate reading, micro-assessment, practice, and recap minutes separately after generating the lesson. Do not force a fixed 45-minute claim.

## 跳过与延伸阅读

List `skip_with_deep_dive` entries:

- **为何跳过** …
- **深入** [label](url) or source location note.

## 微测

3–5 items. **Item 1 must be 预测** (no method hints in the prompt):

1. **预测**：…
2. **用自己的话**：…
3. **应用**（when applicable）：…

Use attempt-first semantics in the assessment plan: place prompts before answer guidance so learners attempt retrieval before inspecting feedback.

- Objective questions: submit a choice, then show correctness and explanation.
- Teach-back questions: submit text, then show a self-check rubric. Keyword coverage is only an aid, never a precise grade.
- Application questions: prefer structured fields when the task has identifiable parts.

Include brief 参考答案 or 评分要点 in this source-traced sidecar for rendering after submission.

## 练习任务

One small practice or transfer task when the section contains procedural, conceptual-transfer, code, tool, or diagnostic content. Include expected checks. Otherwise state that no practice task is needed.

## 复习卡

| 卡片 | 提示 | 掌握层次 | 目标 |
| --- | --- | --- | --- |
| rc1 | … | recall | lo1 |

## 阅读材料（附录）

Bullet list of `reference_only` blocks, useful source links, tables, appendices, or source metadata. These are not exam/core objectives unless explicitly stated.

## 复盘

- 今天节省的时间来自跳过了哪些 filler 或 reference-only 内容？
- 哪张复习卡应该在下一次学习前先做主动回忆？
