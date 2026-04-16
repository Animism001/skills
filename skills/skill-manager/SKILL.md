---
name: skill-manager
description: Manage skills installation, removal, updating, and listing using the npx skills command. Use when the user wants to add, remove, list, find, or update skills, initialize new skills, or sync skills from node_modules. This skill provides guidance on using the --agent trae parameter for npx skills commands and --dir .trae/skills for clawhub commands. Triggers on phrases like "install skill", "remove skill", "list skills", "update skills", "find skills", "initialize skill", "sync skills", or any other skill management tasks.
---

# Skill Manager

A comprehensive guide for managing skills using the `npx skills` command and ClawHub.

## Default Configuration

- **npx skills commands**: Always use `--agent trae` parameter
- **clawhub commands**: Always use `--dir .trae/skills` parameter

## Command Reference

### Manage Skills

```bash
# Add a skill package
npx skills add <package> --agent trae
# Examples:
# npx skills add vercel-labs/agent-skills --agent trae
# npx skills add https://github.com/vercel-labs/agent-skills --agent trae

# Remove installed skills
npx skills remove [skills] --agent trae

# List installed skills
npx skills list
npx skills ls

# Search for skills interactively
npx skills find [query]
```

### Updates

```bash
# Update skills to latest versions
npx skills update [skills...] --agent trae

# Update global skills only
npx skills update -g --agent trae

# Update project skills only
npx skills update -p --agent trae

# Update without prompts
npx skills update -y --agent trae
```

### Project

```bash
# Restore skills from skills-lock.json
npx skills experimental_install

# Initialize a skill (creates <name>/SKILL.md or ./SKILL.md)
npx skills init [name]

# Sync skills from node_modules into agent directories
npx skills experimental_sync --agent trae
```

### Add Options

```bash
# Install skill globally (user-level) instead of project-level
npx skills add <package> -g --agent trae

# Specify agents to install to (use '*' for all agents)
npx skills add <package> -a <agents> --agent trae

# Specify skill names to install (use '*' for all skills)
npx skills add <package> -s <skills> --agent trae

# List available skills in the repository without installing
npx skills add <package> -l --agent trae

# Skip confirmation prompts
npx skills add <package> -y --agent trae

# Copy files instead of symlinking to agent directories
npx skills add <package> --copy --agent trae

# Shorthand for --skill '*' --agent '*' -y
npx skills add <package> --all --agent trae

# Search all subdirectories even when a root SKILL.md exists
npx skills add <package> --full-depth --agent trae
```

### Remove Options

```bash
# Remove from global scope
npx skills remove -g --agent trae

# Remove from specific agents (use '*' for all agents)
npx skills remove -a <agents> --agent trae

# Specify skills to remove (use '*' for all skills)
npx skills remove -s <skills> --agent trae

# Skip confirmation prompts
npx skills remove -y --agent trae

# Shorthand for --skill '*' --agent '*' -y
npx skills remove --all --agent trae
```

### Experimental Sync Options

```bash
# Specify agents to install to (use '*' for all agents)
npx skills experimental_sync -a <agents> --agent trae

# Skip confirmation prompts
npx skills experimental_sync -y --agent trae
```

### List Options

```bash
# List global skills (default: project)
npx skills list -g

# Filter by specific agents
npx skills list -a <agents>

# Output as JSON (machine-readable, no ANSI codes)
npx skills list --json
```

### ClawHub Integration

```bash
# Install a skill to .trae/skills directory
npx clawhub install <slug> --dir .trae/skills

# Update installed skills in .trae/skills
npx clawhub update [slug] --dir .trae/skills

# Uninstall a skill from .trae/skills
npx clawhub uninstall <slug> --dir .trae/skills

# List installed skills in .trae/skills
npx clawhub list --dir .trae/skills
```

## Workflow Guide

### When the user wants to install a skill

1. Determine the skill package to install
2. Use the command: `npx skills add <package> --agent trae`
3. For ClawHub skills, use: `npx clawhub install <slug> --dir .trae/skills`
4. Confirm successful installation

### When the user wants to remove a skill

1. Determine the skill to remove
2. Use the command: `npx skills remove <skill> --agent trae`
3. For ClawHub skills, use: `npx clawhub uninstall <slug> --dir .trae/skills`
4. Confirm successful removal

### When the user wants to update skills

1. Determine if updating all skills or specific ones
2. Use the command: `npx skills update [skills] --agent trae`
3. For ClawHub skills, use: `npx clawhub update [slug] --dir .trae/skills`
4. Confirm successful update

### When the user wants to list installed skills

1. Use the command: `npx skills list`
2. For ClawHub skills, use: `npx clawhub list --dir .trae/skills`
3. Present the list in a clear format

### When the user wants to search for skills

1. Use the command: `npx skills find [query]`
2. For ClawHub skills, use: `npx clawhub search "<query>"`
3. Present the search results

### When the user wants to initialize a new skill

1. Use the command: `npx skills init [name]`
2. Guide the user through creating the SKILL.md file
3. Provide best practices for skill creation

## Important Notes

1. **Always use `--agent trae`** when using `npx skills` commands
2. **Always use `--dir .trae/skills`** when using `clawhub` commands
3. **Ensure the `.trae/skills` directory exists** before installing - create it if necessary with `mkdir -p .trae/skills`
4. When instructing users, always include the appropriate parameters as specified in the user rules

## Examples

```bash
# Install a skill with agent parameter
npx skills add vercel-labs/agent-skills --agent trae

# Install a global skill
npx skills add vercel-labs/agent-skills -g --agent trae

# Install specific skills from a repository
npx skills add vercel-labs/agent-skills --skill pr-review commit --agent trae

# Remove a skill
npx skills remove web-design --agent trae

# Remove from global scope
npx skills rm --global frontend-design --agent trae

# List project skills
npx skills list

# List global skills
npx skills ls -g

# Filter skills by agent
npx skills ls -a claude-code

# JSON output
npx skills ls --json

# Search for skills
npx skills find
npx skills find typescript

# Update all skills
npx skills update --agent trae

# Update a single skill
npx skills update my-skill --agent trae

# Update global skills only
npx skills update -g --agent trae

# Restore from skills-lock.json
npx skills experimental_install

# Initialize a new skill
npx skills init my-skill

# Sync skills from node_modules
npx skills experimental_sync --agent trae
npx skills experimental_sync -y --agent trae
```
