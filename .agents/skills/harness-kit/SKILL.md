---
name: harness-kit
description: Initialize project workspace with OpenClaw harness configuration files. Supports 3 types (default, Claude, Trae). Creates .agents/ with subdirectories (skills/, rules/, workflows/) and root-level MD files. Claude adds CLAUDE.md + .claude/ symlink. Trae adds .trae/ with all symlinks.
version: 1.1.0
---

# harness-kit

Initialize a project workspace with OpenClaw harness configuration files.

## Trigger

When the user asks to:
- Initialize a workspace / project
- Set up harness files / configuration files
- Install OpenClaw workspace templates
- "初始化工作区" / "初始化项目"
- Initialize for Claude / Trae

## What It Does

Creates a `.agents/` directory (with `skills/`, `rules/`, `workflows/` subdirectories) and releases root-level MD files. Type-specific extras are layered on top.

### Core Principle

**实体文件释放是第一优先级。** 所有类型都执行：
1. 创建 `.agents/{skills,rules,workflows}/`
2. 复制 MD 文件到项目根目录

Type-specific 操作是额外的，不包含额外实体文件。

### Types

| Type | Root MD (实体) | `.agents/` subdirs | Extra |
|------|---------------|---------------------|-------|
| `default` | ✓ (AGENTS.md + 7个MD) | ✓ | — |
| `claude` | ✓ (同 default) | ✓ | `CLAUDE.md` (`@AGENTS.md`) + `.claude/ → .agents/` |
| `trae` | ✓ (同 default) | ✓ | `.trae/` (全部符号链接，无实体文件) |

### Directory Structure

**Default:**
```
project/
├── .agents/
│   ├── skills/
│   ├── rules/
│   └── workflows/
├── AGENTS.md          ← 实体文件
├── SOUL.md             ← 实体文件
├── BOOTSTRAP.md        ← 实体文件
├── HEARTBEAT.md        ← 实体文件
├── IDENTITY.md         ← 实体文件
├── TOOLS.md            ← 实体文件
├── USER.md             ← 实体文件
└── MEMORY.md           ← 实体文件
```

**Claude:**
```
project/
├── .agents/
│   ├── skills/
│   ├── rules/
│   └── workflows/
├── .claude -> .agents  ← 符号链接
├── AGENTS.md          ← 实体文件
├── CLAUDE.md          ← 实体文件（内容: @AGENTS.md）
├── SOUL.md ...        ← 实体文件
└── ...
```

**Trae:**
```
project/
├── .agents/
│   ├── skills/
│   ├── rules/
│   └── workflows/
├── .trae/
│   ├── AGENTS.md -> ../AGENTS.md       ← 符号链接
│   ├── SOUL.md -> ../SOUL.md           ← 符号链接
│   ├── BOOTSTRAP.md -> ../BOOTSTRAP.md ← 符号链接
│   ├── HEARTBEAT.md -> ../HEARTBEAT.md ← 符号链接
│   ├── IDENTITY.md -> ../IDENTITY.md   ← 符号链接
│   ├── TOOLS.md -> ../TOOLS.md         ← 符号链接
│   ├── USER.md -> ../USER.md           ← 符号链接
│   ├── MEMORY.md -> ../MEMORY.md       ← 符号链接
│   ├── skills -> ../.agents/skills     ← 符号链接
│   ├── rules -> ../.agents/rules       ← 符号链接
│   └── workflows -> ../.agents/workflows ← 符号链接
├── AGENTS.md          ← 实体文件（根目录）
├── SOUL.md ...        ← 实体文件（根目录）
└── ...
```

> **Trae 特点：`.trae/` 中全部是符号链接，没有任何实体文件。**

### Common Files

| File | Purpose |
|------|---------|
| AGENTS.md | Agent workspace rules |
| SOUL.md | Agent personality and values |
| BOOTSTRAP.md | First-run onboarding guide |
| HEARTBEAT.md | Heartbeat check template |
| IDENTITY.md | Agent identity template |
| TOOLS.md | Local tool notes template |
| USER.md | User information template |
| MEMORY.md | Long-term curated memory |

### Subdirectories

| Directory | Purpose |
|----------|---------|
| skills/ | 技能文件存放目录 |
| rules/ | 规则文件存放目录 |
| workflows/ | 工作流文件存放目录 |

**Key behavior: If a file or directory with the same name already exists, it will NOT be overwritten.** This preserves any user customizations.

## Usage

```bash
bash <skill_dir>/scripts/init.sh [--type <default|claude|trae>] [target_dir]
```

- `--type` — AI type (default: `default`)
- `target_dir` — Target directory (default: current working directory)

### Examples

```bash
# Default initialization
bash init.sh

# Initialize for Claude
bash init.sh --type claude

# Initialize for Trae
bash init.sh --type trae

# Initialize in specific directory
bash init.sh --type trae /path/to/project
```

### Agent Instructions

When this skill is triggered:

1. Ask the user:
   - Which directory to initialize (default to current workspace root)
   - Which AI type (default, claude, or trae)
2. Run the init script with appropriate `--type` parameter
3. Report which files were created and which were skipped
