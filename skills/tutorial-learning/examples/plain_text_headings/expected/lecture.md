---
skill: tutorial-learning
source_format: plain_text_with_headings
section_id: plain_text_headings
learning_objectives: [lo1, lo2]
---

## 本节目标
- `lo1`：用自己的话解释有界重试。
- `lo2`：应用有界重试处理暂时性失败。

## 来源与边界
| source trace id | locator/page/anchor/heading | boundary confidence | evidence type |
| --- | --- | --- | --- |
| `st-txt-main` | Retry Strategy | explicit | source-derived |

## 学习路线
| block title | 角色 | 深度 | 预计分钟 | 说明 |
| --- | --- | --- | --- | --- |
| Retry Strategy | core | standard | 8 | 学习暂时性失败的有界重试。 |

## 核心讲解
有界重试只针对暂时性失败，并限制尝试次数，避免无限循环。核心来源为 `st-txt-main`。

## 跳过与延伸阅读
- 完整错误目录属于查阅材料，本节不展开。

## 微测
1. **预测**：暂时性失败发生后，有界重试会怎样处理？
2. **用自己的话**：解释为什么必须限制尝试次数。
3. **应用**：为一个暂时性错误写出可检查的重试策略。

参考答案：只重试暂时性错误，限制次数，并检查最终结果。

## 练习任务
为网络请求设计最多三次尝试的策略，并检查永久性错误不会被重复执行。

## 复习卡
| 卡片 | 提示 | 掌握层次 | 目标 |
| --- | --- | --- | --- |
| rc1 | 用自己的话解释核心机制。 | recall | lo1 |
| rc2 | 预测一次机制结果。 | application | lo2 |
| rc3 | 应用机制解决一个小问题。 | application | lo1, lo2 |

## 阅读材料（附录）
- 完整错误目录仅用于按需查阅。

## 复盘
- 今天节省的时间来自跳过了哪些 filler 或 reference-only 内容？
- 下一次学习前先主动回忆哪张复习卡？
