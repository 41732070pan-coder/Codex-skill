# Codex-skill

一个用于沉淀、工程化管理和持续演进个人 Codex Skills 的仓库。当前仓库从“单个设计风格 Skill”升级为“多 Skill 工作区”：既包含可直接使用的业务 Skill，也包含一个用于约束和生成其他 Skill 的顶层治理 Skill。

## 项目定位

本仓库的目标不是收集零散提示词，而是把每个 Skill 当作可维护的软件模块管理：

- 用统一目录结构组织不同能力，例如视觉设计、AI 辅助学习、研究写作、代码审查等未来 Skill。
- 用接口、注册表、模板、状态机、策略模式、质量门禁等编程思想描述 Skill 的边界和扩展点。
- 让 Codex 在使用 Skill 时可以按需加载少量上下文，而不是一次读取整个仓库。
- 为每个 Skill 保留清晰的触发条件、输入输出、素材归属、扩展流程和自检规则。

## 顶层工程哲学：Skill 的 Skill

仓库新增 `skill-governance` 作为“Skill 的 Skill”。它不是面向某个单一产物的业务能力，而是用于设计、审查和重构其他 Skill 的顶层工程约束。

`skill-governance` 规定：

- **Skill 不是一个长 Prompt**：它应被建模为包含接口、数据结构、策略、资产、质量门禁和生命周期的小型能力模块。
- **`SKILL.md` 是编排层**：负责触发边界、通用流程和不变量；领域细节应下沉到 `references/`。
- **多实现必须有注册表**：当一个 Skill 拥有多个风格、学习法、输出模式或工具提供者时，应使用 `*_registry.md` 显式登记。
- **扩展优先使用设计模式**：优先考虑 Template Method、Strategy、Registry、Factory、Adapter、Composite、State Machine、Quality Gate，而不是在说明文字中堆叠特例。
- **资产必须有归属**：素材只属于某个 Skill 或明确声明的共享提供器，避免跨 Skill 滥用品牌、版权或语义资产。

详细约束见 `skills/skill-governance/SKILL.md` 和 `skills/skill-governance/references/top_level_skill_constraints.md`。

## 当前 Skill 清单

| Skill | 类型 | 位置 | 用途 | 状态 |
| --- | --- | --- | --- | --- |
| `skill-governance` | 元 Skill / 工程治理 | `skills/skill-governance/` | 为新增、重构、审查 Skill 提供顶层约束、数据模型、设计模式和质量门禁 | 稳定基础版 |
| `my-design-style` | 业务 Skill / 设计系统 | `skills/my-design-style/` | 为 PPT、网页、App、Dashboard、静态视觉稿等产物提供可扩展视觉风格系统 | 可用 |

未来可以继续添加：

- `ai-learning-coach`：AI 辅助学习 Skill，用状态机管理诊断、计划、练习、复盘和间隔复习。
- `research-writing`：研究写作 Skill，用资料卡片、论证图和引用质量门禁管理写作流程。
- `code-review-coach`：代码审查 Skill，用风险分类、检查表和语言/框架策略管理审查输出。

这些新增 Skill 都应先经过 `skill-governance` 的结构化建模，再落地为具体目录。

## 推荐目录结构

```text
.
├── README.md
└── skills/
    ├── skill-governance/
    │   ├── SKILL.md
    │   ├── agents/
    │   │   └── openai.yaml
    │   └── references/
    │       └── top_level_skill_constraints.md
    └── my-design-style/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        ├── assets/
        │   └── seu_design_style/
        │       ├── ASSET_MANIFEST.md
        │       └── *.svg
        └── references/
            ├── chinese_traditional_color_style.md
            ├── design_mechanics.md
            ├── renminbi_color_style.md
            ├── seu_design_style.md
            ├── style_contract.md
            ├── style_registry.md
            └── style_template.md
```

## Skill 工程化规范

每个新 Skill 默认应遵循以下结构：

```text
skills/<skill-name>/
├── SKILL.md
├── agents/
│   └── openai.yaml              # 可选：OpenAI/Codex 环境显示信息
├── references/
│   ├── *_contract.md            # 接口、数据结构、输入输出契约
│   ├── *_registry.md            # 策略、风格、模板、工具提供者注册表
│   ├── *_template.md            # 新增同类实现时使用的模板
│   └── *.md                     # 按需加载的领域知识
├── assets/                      # 可选：该 Skill 独占素材
└── examples/                    # 可选：示例、fixtures、验证样例
```

`SKILL.md` 至少应包含：

1. YAML front matter：`name` 和 `description`。
2. 触发条件与非触发条件。
3. 标准工作流或编程模型。
4. 输入输出数据结构或接口。
5. 扩展点、注册机制和模板说明。
6. 质量门禁与自检规则。
7. 素材、外部依赖和法律/版权约束。

## `my-design-style` 简介

`my-design-style` 是当前主要业务 Skill。它不是单一配色表，而是一个可扩展视觉设计框架：

- `SKILL.md` 作为抽象基类与编排层，定义风格解析、设计请求归一化、素材策略、质量检查等通用流程。
- `references/style_contract.md` 定义稳定的数据结构与接口契约。
- `references/style_registry.md` 注册当前可用的具体风格，并说明风格选择规则。
- `references/design_mechanics.md` 收纳跨风格复用的设计机制，例如同色系色阶、素材导入约束、纹理使用原则等。
- `references/<style_name>.md` 是具体风格实现，每个风格都需要实现触发器、设计意图、配色、字体、布局、媒介翻译、素材策略、纹理策略和自检标准。
- `assets/<style_name>/` 存放风格自有素材；当前已内置东南大学风格素材集。

### 已注册设计风格

| 风格名 | 参考文件 | 适用场景 | 素材情况 |
| --- | --- | --- | --- |
| `seu_design_style` | `skills/my-design-style/references/seu_design_style.md` | 东南大学、学术汇报、论文答辩、科研项目、校园品牌相关 PPT / Web / App 设计 | 已内置 SEU 标识、字标、校训、建筑轮廓、松树等 SVG 素材 |
| `renminbi_color_style` | `skills/my-design-style/references/renminbi_color_style.md` | 人民币、金融、价值表达、商业、收藏、拍卖、金融科技和中式价值感场景 | 不绑定官方货币图像；以配色、纹样感和版式语言表达 |
| `chinese_traditional_color_style` | `skills/my-design-style/references/chinese_traditional_color_style.md` | 中国传统色、新中式、国风、博物馆、文化出版、茶/手作/诗词等文化场景 | 不绑定固定身份素材；强调命名色彩体系和现代可用性 |

## 使用方式

### 使用治理 Skill 设计新 Skill

```text
使用 skill-governance，帮我设计一个 ai-learning-coach Skill。
它需要支持学习目标诊断、学习计划、练习生成、错题复盘和间隔复习。
请先给出目录结构、数据模型、状态机、注册表和质量门禁。
```

### 使用视觉设计 Skill

```text
使用 my-design-style，把这份研究汇报做成 seu_design_style 的答辩 PPT 风格。
```

```text
使用 my-design-style。
目标媒介：dashboard
具体风格：renminbi_color_style
内容目标：展示季度营收、成本、现金流和风险指标
受众：公司管理层
输出要求：Web 首屏，深浅色都要有可读性，包含 KPI 卡片、趋势图、风险列表和筛选器。
```

## 新增 Skill 流程

1. 先使用 `skill-governance` 归一化能力目标，明确触发边界、输入输出和质量门禁。
2. 在 `skills/<skill-name>/` 下创建 `SKILL.md`。
3. 如果存在多个策略、模板、风格、模式或工具提供者，新增 `references/*_contract.md`、`references/*_registry.md` 和 `references/*_template.md`。
4. 如果需要素材，放入该 Skill 自己的 `assets/`，并补充素材清单、来源和使用限制。
5. 在本 README 的 Skill 清单和目录结构中登记新 Skill。
6. 至少运行 `git diff --check`；如 Skill 包含代码、脚本或示例产物，应补充对应测试命令。

## 素材策略

当前仓库内置的业务素材集中在 `skills/my-design-style/assets/seu_design_style/`，并由 `ASSET_MANIFEST.md` 明确列出用途、尺寸比例、颜色模式和安全摆放方式。

使用素材时应遵守：

- 只使用当前激活 Skill 和具体策略拥有的素材，不跨 Skill 借用标识、字标或装饰元素。
- Logo、字标、校训、建筑轮廓、松树等身份素材必须保持原始比例，不得非等比拉伸。
- `ASSET_MANIFEST.md` 中标记为 `repeatable` 的图案可重复或裁切，但仍不能非等比缩放。
- 没有合适素材时，应优先使用布局、字体、色彩和代码原生几何，而不是下载通用装饰图。

> 注意：`my-design-style` 的文档中预留了共享透明纹理提供器 `assets/transparent_textures/` 的接口说明，但当前仓库尚未包含该目录。实际使用时应以仓库内已存在的素材和各风格的 `SurfaceTexturePolicy` 为准。

## 维护建议

- 新增或重构任何 Skill 前，优先阅读 `skills/skill-governance/SKILL.md`。
- 保持 Skill 之间边界清晰：业务规则留在业务 Skill，工程治理规则留在 `skill-governance`。
- 配色、教学法、评审策略、工具适配等多实现能力都应注册化，而不是写成隐式分支。
- 更新素材时同步维护对应的素材清单或 manifest。
- README 只保留仓库级说明；具体 Skill 的详细规则应沉淀到各自目录。

## 当前仓库状态

- 当前项目以 Markdown 规范文档和 SVG 资产为主，没有应用运行时代码、构建脚本或自动化测试配置。
- 本仓库适合作为个人 Codex Skill 工作区，也适合作为未来多 Skill 能力库的工程化模板。
