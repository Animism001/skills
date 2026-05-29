---
name: harness-kit
description: Initialize project workspace with OpenClaw harness config files. Skips existing files. Symlinks AGENTS.md to .trae/rules/ for Trae IDE integration.
version: 2.0.0
---

# harness-kit

Initialize a project workspace with OpenClaw harness configuration files.

## Trigger

When the user asks to:
- Initialize a workspace / project
- Set up harness files / configuration files
- Install OpenClaw workspace templates
- "初始化工作区" / "初始化项目"

## What It Does

1. Copies template files from `references/` to the **project root directory**
2. Creates `.trae/rules/` and symlinks `AGENTS.md` there for Trae IDE integration

### Template Files

| File | Purpose |
|------|---------|
| AGENTS.md | Workspace rules and agent behavior |
| SOUL.md | Agent personality and values |
| BOOTSTRAP.md | First-run onboarding guide |
| HEARTBEAT.md | Heartbeat check template |
| IDENTITY.md | Agent identity template |
| TOOLS.md | Local tool notes template |
| USER.md | User information template |

**Existing files are NOT overwritten**, preserving user customizations.

### Trae IDE Integration

After copying files, the script automatically:
- Creates `.trae/rules/` directory
- Symlinks `.trae/rules/AGENTS.md` → `<project_root>/AGENTS.md`

This makes AGENTS.md visible to Trae IDE as a project rule. The symlink ensures a single source of truth — edits to either path update the same file.

If the symlink already exists and points correctly, it is skipped. If it points elsewhere, it is updated. If a regular file exists at that path, it is not overwritten.

## Usage

```bash
bash <skill_dir>/scripts/init.sh [target_dir]
```

- `target_dir` — Target directory (default: current working directory)

### Agent Instructions

1. Ask the user which directory to initialize (default to current workspace root if not specified)
2. Run the init script targeting that directory
3. Report which files were created, skipped, and linked
