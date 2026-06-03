# 中国传统色风格 · 工作流指南 PPT（示例）

用 `my-design-style` skill 的 `chinese_traditional_color_style` 风格生成的演示文稿，
内容改编自 `指南.md` 草稿（已在出片时修订完善）。

## 产物

- `chinese_traditional_guide_deck.pptx` — 9 页 16:9 可编辑 PPT
- `build_deck.py` — 可复现的构建脚本（python-pptx + Pillow）
- `assets/paper_texture.png` — 运行时生成的米纸纹理底（对应 `rice-paper` 纹理 token）

## 风格锁定（StyleLock）

| 维度 | 选择 |
| --- | --- |
| 色卡 | Museum Calm 配方：靛青学者（靛青 #177CB0 / 靛蓝 #065279）+ 墨纸 |
| 点睛色 | 金色 #EACD76 细线、胭脂 #9D2933 印章红（仅作节奏锚点） |
| 字体 | 宋体（编辑标题）、微软雅黑（正文/标题）、楷体（引语/印章） |
| 纹理 | rice-paper 纸纹，浅色面，opacity 区间内；深色结尾页不铺纹理 |
| 版式 | 12 列思维、左侧靛蓝竖栏 + 序号印章、每页一个非正文视觉锚点 |

## 页序

1. 封面 — 竖排宋体标题 + 印章
2. 色卡图例 — 6 色命名色卡 + 用途说明
3. 目录 — 五章节卡片
4. 工作流总览 — Agent + Skill + MCP 三件套
5. 选型建议 — 智能体 / 大模型推荐档位
6. 安装与调用 — 三步 + 触发示例
7. 产物与格式 — SVG / PPT / PDF
8. 微调的边界 — 交给 AI vs 自己动手
9. 结尾 — 靛蓝整页 + 金线 + 印章

## 重新生成

```bash
python build_deck.py
```

## 质量门（已通过）

- `python skills/my-design-style/scripts/validate_styles.py`
- `python skills/meta-skill/scripts/validate_skills.py`
- 几何核验：所有形状均在 13.333 × 7.5 画布内，无溢出

> 注：成稿仍可能有像素级偏移，按指南建议，最后一两步精修应在 PowerPoint 内手动完成，不依赖 AI。
