# 教程结构

## 教学模式

`chapter_tutorial`：当前来源支持一个窄范围 lesson。

## 章节知识地图

Markdown Overview → `build` 基础命令 → `build --fast` 参数实验 → 选项表查阅。

## 课时设计

| lesson | 原型 | 核心概念 | 诊断 | 练习 | 来源层级 |
| --- | --- | --- | --- | --- | --- |
| `lesson-markdown-build` | `tool_operation` | Markdown Basics | 预测 + 解释 + 迁移 | 可检查任务 | `code` |

## 下游渲染交接

下游渲染器可以将 lesson 映射为页面、幻灯片、H5 屏幕或文档章节，但不得改变证据边界、目标覆盖、学习顺序或尝试优先规则。lesson id、诊断反馈、复习任务和代码实验类型是 renderer 可消费的语义钩子。
