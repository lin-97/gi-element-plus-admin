# agents/ — AI 编码助手通用规范

本目录是 **Single Source of Truth（唯一事实来源）**，规范内容不绑定 Cursor 专有格式，可直接给 Cursor、OpenCode、Codex 等工具使用。

## 目录结构

```
agents/
├── README.md                 # 本文件
├── rules/                    # 开发规范（按目录/文件类型生效）
│   ├── frontend-standards.md
│   ├── gi-component-vue.md
│   └── backend-standards.md
└── skills/                   # 任务型技能（按触发词加载）
    ├── git-commit/
    │   ├── SKILL.md
    │   └── examples.md
    └── table-page/
        └── SKILL.md
```

## 各工具接入

### 统一入口

所有工具优先读取仓库根目录 [`AGENTS.md`](../AGENTS.md)，再按任务类型加载 `agents/rules/` 与 `agents/skills/` 下对应文件。

### Codex / 通用 Agent

将 `AGENTS.md` 设为项目指令入口即可。

### OpenCode

在项目配置中引用根目录 `AGENTS.md`，或将 `agents/rules/*.md` 加入 instructions：

```jsonc
{
  "instructions": [
    "AGENTS.md",
    "agents/rules/frontend-standards.md"
  ]
}
```

Skills 可映射为 OpenCode skill，正文指向 `agents/skills/*/SKILL.md`。

### Cursor

在 Cursor 项目设置中将 `AGENTS.md` 加入 Rules / Instructions，或启用对根目录 `AGENTS.md` 的自动读取（若版本支持）。规范正文均在 `agents/`，无需维护 `.cursor/rules` 或 `.cursor/skills` 下的重复副本。

## 维护约定

- **只改 `agents/`**，并在 `AGENTS.md` 索引中登记新增 rule / skill
- 新增 rule：放入 `agents/rules/`
- 新增 skill：放入 `agents/skills/{name}/SKILL.md`
- Skill 元数据使用通用 YAML frontmatter（`name`、`description`、`triggers`）

## 复制到其他项目

将整个 `agents/` 目录与根目录 `AGENTS.md` 复制到目标仓库，按项目实际情况修改：

- 技术栈与目录约定
- 参考实现路径
- Git 提交 type 与仓库结构
