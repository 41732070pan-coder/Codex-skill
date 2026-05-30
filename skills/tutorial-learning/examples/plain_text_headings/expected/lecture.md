---
skill: tutorial-learning
source_format: plain_text_with_headings
source_title: "Retry Strategy"
source_locator: "source.txt"
section_id: plain_text_headings
section_title: "Retry Strategy"
design_mode: chapter_tutorial
evidence_granularity: paragraph
lesson_count: 1
est_minutes_total: 8
learning_objectives:
  - id: lo1
    text: "解释核心机制。"
    mastery: recall
    verifiable: "能够用自己的话说明。"
    source_trace_ids: [st-txt-main]
  - id: lo2
    text: "应用核心机制。"
    mastery: application
    verifiable: "能够完成一个小任务。"
    source_trace_ids: [st-txt-main]
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
- `lesson-retry-bounded`：瞬时故障识别 → 有界重试次数 → 停止条件 → 完整错误目录作为查阅材料。

## 本节目标
- `lo1`：解释核心机制。
- `lo2`：应用核心机制。

## 来源与边界
| source trace id | locator/page/anchor/heading | granularity | boundary confidence | evidence type |
| --- | --- | --- | --- | --- |
| `st-txt-main` | source.txt | paragraph | explicit | source-derived |

## 学习路线
| lesson | 原型 | 深度 | 预计分钟 | 说明 |
| --- | --- | --- | --- | --- |
| `lesson-retry-bounded` | `optimization_diagnosis` | standard | 8 | 只覆盖来源支持的核心机制。 |

## 核心讲解
### Lesson lesson-retry-bounded：Retry Strategy

来源规则是：对瞬时故障执行重试，但尝试次数必须有上限。重点不是“永远重试”，而是同时满足故障类型判断和有界停止条件。核心证据为 `st-txt-main`。

**正例**：瞬时故障在有限次数内重试，达到上限后停止。

**反例**：对任何错误无限重试。

**常见误区**：把来源范围外的泛化知识当成当前来源已经证明的内容。

**下一课桥接**：完成当前检查后，再按来源扩展决定是否增加后续 lesson。

## 跳过与延伸阅读
- 低价值噪声不进入核心教学；查阅型内容保留在附录。

## 诊断反馈
- 诊断能力：能否基于来源完成 `Retry Strategy` 的核心判断。
- 错误反馈：若答案缺少次数上限，回到 bounded attempt count 并补充停止条件。

## 微测
1. **预测**：如果故障持续存在，为什么有界尝试比无限重试更安全？给出停止条件。
2. **用自己的话**：说明本节规则及其证据边界。
3. **迁移**：给出一个相邻场景，并说明哪些判断仍然适用。

参考答案或评分要点：回答必须覆盖核心规则、可检查结果和来源边界。

## 练习任务
为一次瞬时故障写出带最大尝试次数的重试决策，并说明达到上限后的停止行为。

验收：能同时写出瞬时故障条件、最大尝试次数和停止行为。

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
