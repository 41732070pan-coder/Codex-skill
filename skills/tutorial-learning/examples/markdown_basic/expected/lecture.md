---
skill: tutorial-learning
source_format: markdown
source_title: "Markdown Basics"
source_locator: "source.md"
section_id: markdown_basic
section_title: "Markdown Basics"
design_mode: chapter_tutorial
evidence_granularity: code
lesson_count: 1
est_minutes_total: 8
learning_objectives:
  - id: lo1
    text: "解释核心机制。"
    mastery: recall
    verifiable: "能够用自己的话说明。"
    source_trace_ids: [st-md-main]
  - id: lo2
    text: "应用核心机制。"
    mastery: application
    verifiable: "能够完成一个小任务。"
    source_trace_ids: [st-md-main]
triage_summary:
  core_blocks: 1
  skipped_blocks: 1
  appendix_blocks: 0
---

## 教学模式与证据边界
- 模式：`chapter_tutorial`。
- 最强证据层级：`code`。
- 当前是窄范围来源，因此只设计 1 个证据充分的 lesson；不使用重复模板补足数量。

## 章节知识地图
- `lesson-markdown-build`：Markdown Overview → `build` 基础命令 → `build --fast` 参数实验 → 选项表查阅。

## 本节目标
- `lo1`：解释核心机制。
- `lo2`：应用核心机制。

## 来源与边界
| source trace id | locator/page/anchor/heading | granularity | boundary confidence | evidence type |
| --- | --- | --- | --- | --- |
| `st-md-main` | source.md | paragraph | explicit | source-derived |
| `st-md-code` | source.md | code | explicit | source-derived |

## 学习路线
| lesson | 原型 | 深度 | 预计分钟 | 说明 |
| --- | --- | --- | --- | --- |
| `lesson-markdown-build` | `tool_operation` | standard | 8 | 只覆盖来源支持的核心机制。 |

## 核心讲解
### Lesson lesson-markdown-build：Markdown Basics

本节的核心动作是运行 `build`。来源还给出了代码级示例 `build --fast` 和选项表：`--fast` 表示更快执行。学习时先区分基础命令与可选参数，再比较是否添加 `--fast`。核心解释追踪到 `st-md-main`，命令实验追踪到 `st-md-code`。

**正例**：先识别基础命令 `build`，再把 `--fast` 作为可选参数加入。

**反例**：把 `--fast` 当成独立命令，忽略它依附于 `build`。

**常见误区**：把来源范围外的泛化知识当成当前来源已经证明的内容。

**下一课桥接**：完成当前检查后，再按来源扩展决定是否增加后续 lesson。

## 跳过与延伸阅读
- 低价值噪声不进入核心教学；查阅型内容保留在附录。

## 诊断反馈
- 诊断能力：能否基于来源完成 `Markdown Basics` 的核心判断。
- 错误反馈：若把参数误当命令，回到选项表并拆分命令名与参数。

## 微测
1. **预测**：阅读 `build --fast`：指出命令与参数，并预测去掉 `--fast` 后哪项行为会变化。
2. **用自己的话**：说明本节规则及其证据边界。
3. **迁移**：给出一个相邻场景，并说明哪些判断仍然适用。

参考答案或评分要点：回答必须覆盖核心规则、可检查结果和来源边界。

## 练习任务
执行或纸面模拟 `build` 与 `build --fast` 两个命令；运行前预测差异，再记录 `--fast` 对应的预期变化。

验收：能说明 `build` 是基础命令、`--fast` 是可选参数，并根据来源表格解释预期差异。

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
