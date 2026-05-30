# Lecture Template (Chinese)

Use this shape for each section lecture. YAML front matter is required.

```yaml
---
skill: tutorial-learning
medium: pdf-chaptered
source_title: "<book title>"
source_url: "<url>"
section_id: "<e.g. ch01-s01>"
section_title: "<Chinese section title>"
h5_lesson_id: "<medium>-<slug>-<section_id>"
est_minutes_total: <number>
learning_objectives:
  - id: lo1
    text: "<Chinese objective>"
    mastery: exposure|recall|application
    verifiable: "<how to verify>"
triage_summary:
  core_blocks: <n>
  skipped_blocks: <n>
  appendix_blocks: <n>
---
```

## 本节目标

2–4 bullets tied to `learning_objectives`.

## 学习路线

**Required.** Short table: block title | 深度 | 预计分钟 | 说明

Column `深度` must use: skip | skim | standard | deep.

## 核心讲解

Ordered subsections for `core` and in-lecture `supporting` blocks.

- Teach mechanism, not copy-paste from PDF.
- Use 中文; keep API names, commands, formulas in original form.
- For `skim` blocks: ≤ 1 short paragraph.

## 跳过与延伸阅读

List `skip_with_deep_dive` entries:

- **为何跳过** …
- **深入** [label](url)

## 微测

3–5 items. **Item 1 must be 预测** (no method hints in the prompt):

1. **预测**：…
2. **用自己的话**：…
3. **应用**（optional）：…

Include brief 参考答案 or 评分要点.

## 复习卡

| 卡片 | 提示 | 掌握层次 |
| --- | --- | --- |
| rc1 | … | recall |

## 阅读材料（附录）

Bullet list of `reference_only` items — not exam core.

## 复盘

- 今天节省的时间来自跳过了哪些 filler？
- 下一节建议先复习哪张卡片？
