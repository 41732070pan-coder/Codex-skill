---
skill: tutorial-learning
source_format: pdf
source_title: "PDF Excerpt"
source_locator: "source.txt"
section_id: pdf_excerpt_noisy
section_title: "PDF Excerpt"
design_mode: chapter_tutorial
evidence_granularity: paragraph
lesson_count: 1
est_minutes_total: 8
learning_objectives:
  - id: lo1
    text: "解释核心机制。"
    mastery: recall
    verifiable: "能够用自己的话说明。"
    source_trace_ids: [st-pdf-main]
  - id: lo2
    text: "应用核心机制。"
    mastery: application
    verifiable: "能够完成一个小任务。"
    source_trace_ids: [st-pdf-main]
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
- `lesson-pdf-mechanism`：页眉排除 → `Chapter concept` 边界 → `The mechanism matters.` 核心句 → 页脚排除。

## 本节目标
- `lo1`：解释核心机制。
- `lo2`：应用核心机制。

## 来源与边界
| source trace id | locator/page/anchor/heading | granularity | boundary confidence | evidence type |
| --- | --- | --- | --- | --- |
| `st-pdf-main` | source.txt | paragraph | explicit | source-derived |

## 学习路线
| lesson | 原型 | 深度 | 预计分钟 | 说明 |
| --- | --- | --- | --- | --- |
| `lesson-pdf-mechanism` | `conceptual` | standard | 8 | 只覆盖来源支持的核心机制。 |

## 核心讲解
### Lesson lesson-pdf-mechanism：PDF Excerpt

可确认的正文只有 `Chapter concept` 和 `The mechanism matters.`。因此本节只训练学习者识别正文边界与机制重要性，不补写来源未提供的机制步骤。核心证据为 `st-pdf-main`。

**正例**：把正文核心句与页眉页脚分离。

**反例**：根据标题自行补写机制实现细节。

**常见误区**：把来源范围外的泛化知识当成当前来源已经证明的内容。

**下一课桥接**：完成当前检查后，再按来源扩展决定是否增加后续 lesson。

## 跳过与延伸阅读
- 低价值噪声不进入核心教学；查阅型内容保留在附录。

## 诊断反馈
- 诊断能力：能否基于来源完成 `PDF Excerpt` 的核心判断。
- 错误反馈：若答案补写了来源没有提供的步骤，降级为受限概括并请求更多段落。

## 微测
1. **预测**：指出哪些文字属于正文，并说明为什么当前证据不足以展开机制步骤。
2. **用自己的话**：说明本节规则及其证据边界。
3. **迁移**：给出一个相邻场景，并说明哪些判断仍然适用。

参考答案或评分要点：回答必须覆盖核心规则、可检查结果和来源边界。

## 练习任务
标记摘录中的页眉、正文和页脚，并写出一句不超出来源证据的教学概括。

验收：能保留核心句、排除页眉页脚，并避免虚构机制细节。

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
