# 中国传统色风格 · 工作流指南 PPT（示例）

用 `my-design-style` skill 的 `chinese_traditional_color_style` 风格生成的演示文稿，
内容改编自 `指南.md` 草稿（已在出片时修订完善）。

## 产物

- `chinese_traditional_guide_deck.pptx` — 9 页 16:9 可编辑 PPT
- `build_deck.py` — 可复现的构建脚本（python-pptx + Pillow + svglib + reportlab）
- `assets/` — 运行时光栅化的 RGBA 资产与纹理底（见下）
- `asset_use_check.json` — 交付时产出的 `AssetUseCheck` 质量门输出

## 资产使用（asset-rich，AssetUseCheck）

本示例遵循 `my-design-style` 的 asset-rich 默认：不走纯 code-native，而是接入风格自带 SVG 资产与共享纹理 provider。因为 python-pptx 不能直接嵌入 SVG，脚本用 `svglib + reportlab` 将 SVG 光栅化为 **RGBA PNG（保留透明通道）**——双背景合成法恢复真 alpha，深色页用黑底色源、浅色页用白底色源，确保边缘无白底/黑底光晕。

| 资产 | 来源 | 角色 | 出现位置 | 处理 |
| --- | --- | --- | --- | --- |
| rice-paper | 共享 provider `transparent_textures` | 纸纹页底 | 所有浅色页 | 解出内嵌 PNG tile 平铺，opacity≈0.07 |
| 圆形方孔钱 | 风格自带 SVG | 价值 / 选型意象 | 封面 | 原生靛蓝双色，光栅化 |
| 中国结 | 风格自带 SVG | 连接 / 协作意象 | 工作流页 | 原生靛蓝双色，光栅化 |
| 云纹 | 风格自带 SVG | 留白 / 意境淡纹 | 封面靛蓝块 | 重着色为藏青，opacity 0.4 |
| 回纹边框 | 风格自带 SVG | 结尾顶部纹饰 | 结尾页 | 重着色为金色（深色页） |

`asset_use_check.json` 记录 `distinctAssetCount`、`countWithinTarget`、以及 `transparencyPreserved / aspectRatioPreserved / readabilityPreserved / semanticRelevance / rasterizationClean` 等质量标志，作为质量门检查项。资产数量为引导（5-10）而非硬配额，克制风格取低端、保证每个资产都有语义角色即可。

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
