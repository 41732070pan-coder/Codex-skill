# 教程结构

## 教学模式

`chapter_tutorial`：当前来源支持一个窄范围 lesson。

## 章节知识地图

瞬时故障识别 → 有界重试次数 → 停止条件 → 完整错误目录作为查阅材料。

## 课时设计

| lesson | 原型 | 核心概念 | 诊断 | 练习 | 来源层级 |
| --- | --- | --- | --- | --- | --- |
| `lesson-retry-bounded` | `optimization_diagnosis` | Retry Strategy | 预测 + 解释 + 迁移 | 可检查任务 | `paragraph` |

## 下游渲染交接

下游渲染器可以将 lesson 映射为页面、幻灯片、H5 屏幕或文档章节，但不得改变证据边界、目标覆盖、学习顺序或尝试优先规则。lesson id、诊断反馈、复习任务和代码实验类型是 renderer 可消费的语义钩子。
