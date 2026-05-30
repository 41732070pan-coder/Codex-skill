---
skill: tutorial-learning
source_format: html
source_title: "HTML Noise Filtering"
source_locator: "source.html"
section_id: html_with_noise
section_title: "HTML Noise Filtering"
design_mode: chapter_tutorial
evidence_granularity: paragraph
lesson_count: 1
est_minutes_total: 8
learning_objectives:
  - id: lo1
    text: "解释核心机制。"
    mastery: recall
    verifiable: "能够用自己的话说明。"
    source_trace_ids: [st-html-main]
  - id: lo2
    text: "应用核心机制。"
    mastery: application
    verifiable: "能够完成一个小任务。"
    source_trace_ids: [st-html-main]
triage_summary:
  core_blocks: 1
  skipped_blocks: 1
  appendix_blocks: 0
---

## 教学模式与证据边界
- 模式：`chapter_tutorial`。
- 最强证据层级：`paragraph`。
- 当前是窄范围来源，因此只设计 1 个证据充分的 lesson；不使用重复模板补足数量。

## 章节知识地图
- `lesson-html-main`：主体内容隔离 → 保留可学习解释 → 排除导航、广告和 cookie banner。

## 本节目标
- `lo1`：解释核心机制。
- `lo2`：应用核心机制。

## 来源与边界
| source trace id | locator/page/anchor/heading | granularity | boundary confidence | evidence type |
| --- | --- | --- | --- | --- |
| `st-html-main` | source.html | paragraph | explicit | source-derived |

## 学习路线
| lesson | 原型 | 深度 | 预计分钟 | 说明 |
| --- | --- | --- | --- | --- |
| `lesson-html-main` | `conceptual` | standard | 8 | 只覆盖来源支持的核心机制。 |

## 核心讲解
### Lesson lesson-html-main：HTML Noise Filtering

HTML 教程抽取的关键不是保留所有可见文字，而是识别正文边界。来源段落 `Keep this explanation.` 位于 `<main>` 内，因此作为核心解释保留；导航、广告和 cookie banner 不进入核心讲解。核心证据为 `st-html-main`。

**正例**：保留 `<main>` 中的解释段落。

**反例**：把 `<nav>`、`<aside>` 和 cookie banner 当成课程正文。

**常见误区**：把来源范围外的泛化知识当成当前来源已经证明的内容。

**下一课桥接**：完成当前检查后，再按来源扩展决定是否增加后续 lesson。

## 跳过与延伸阅读
- 低价值噪声不进入核心教学；查阅型内容保留在附录。

## 诊断反馈
- 诊断能力：能否基于来源完成 `HTML Noise Filtering` 的核心判断。
- 错误反馈：若把导航或广告纳入正文，回到正文容器与 filler 角色的区别。

## 微测
1. **预测**：判断 `<main>`、`<nav>`、`<aside>` 和 cookie banner 中哪些内容应进入课程正文，并解释依据。
2. **用自己的话**：说明本节规则及其证据边界。
3. **迁移**：给出一个相邻场景，并说明哪些判断仍然适用。

参考答案或评分要点：回答必须覆盖核心规则、可检查结果和来源边界。

## 练习任务
从给定 HTML 中列出应保留与应排除的块，并用正文容器和内容角色解释判断。

验收：能保留 `<main>` 中的解释，并排除导航、广告和 cookie banner。

## 复习卡
| 卡片 | 提示 | 掌握层次 | 目标 |
| --- | --- | --- | --- |
| rc1 | 用自己的话解释核心规则。 | recall | lo1 |
| rc2 | 预测一次机制结果。 | application | lo2 |
| rc3 | 判断一个相邻场景是否适用。 | application | lo1, lo2 |

## 阅读材料（附录）
- 省略的 filler 和 reference-only 内容不作为核心目标。

## 复盘
- 当前 lesson 的证据层级允许讲到多深？
- 错误答案应转成哪张复习卡？
