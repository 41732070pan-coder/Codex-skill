# Codex-skill

个人 Codex Skills 工作区，用于沉淀可复用、可维护的技能模块，而不是收集零散提示词。

## 仓库定位

本仓库把每个 Skill 作为一个小型能力模块管理：它应具有清晰的触发条件、输入输出、参考资料、素材归属、扩展点和质量门禁。设计、重命名、审查或重构 Skill 时使用 `meta-skill`；当某个 Skill 内部存在可扩展的多实现族（如风格、策略、Provider、Adapter、模式）时，也由 `meta-skill` 约束其注册表、脚本化发现和按需加载边界；执行具体领域任务时使用对应业务 Skill。

本仓库不鼓励为一次性、低复用、无扩展需求的简单提示创建 Skill；这类能力通常应保留在普通对话、项目说明或局部脚本中。`meta-skill` 面向值得长期沉淀、维护和扩展的能力模块，而不是为所有简单任务提供治理流程。

## 已有 Skills

| Skill | 类型 | 位置 | 功能 | 状态 |
| --- | --- | --- | --- | --- |
| `meta-skill` | 元 Skill / 治理 | `skills/meta-skill/` | 设计、添加、重命名、审查、重构和治理仓库内的 Skills 与多实现族，提供契约、注册表、模板、加载边界、生命周期和质量门禁规则。 | stable |
| `my-design-style` | 业务 Skill / 视觉设计 | `skills/my-design-style/` | 为 PPT、网页、App、Dashboard、静态视觉稿和设计模板应用可扩展视觉风格系统。 | experimental |

## 高层目录结构

```text
.
├── README.md
└── skills/
    ├── meta-skill/
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   ├── references/
    │   └── scripts/
    └── my-design-style/
        ├── SKILL.md
        ├── agents/openai.yaml
        ├── assets/
        └── references/
```

## 新增或修改 Skill

1. 先使用 `meta-skill` 明确能力目标、触发边界、输入输出、资源策略、扩展点和质量门禁。
2. 每个维护中的 Skill 放在 `skills/<skill-name>/` 下。
3. `SKILL.md` 只保留编排、触发条件、工作流和不变量。
4. 详细契约、注册表、模板和领域资料放入 `references/`；可增长的多实现族应通过注册表和 list/resolve/get 脚本发现并按需加载。
5. 素材放入所属 Skill 的 `assets/`；跨 Skill 共享素材必须有明确共享提供器。
6. 更新本 README 的 Skill 列表，以及 `skills/meta-skill/references/skill_registry.md`。
7. 至少运行 `python skills/meta-skill/scripts/validate_skills.py`、`python skills/meta-skill/scripts/validate_skill_boundaries.py` 和 `git diff --check`；如果 Skill 包含脚本、示例产物或可运行代码，应补充对应测试。
