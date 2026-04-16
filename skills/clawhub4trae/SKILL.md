---
name: clawhub4trae
description: Search, discover, install, and manage skills on ClawHub (clawhub.ai) specifically for Trae agents. Use when the user wants to find skills, discover new capabilities, browse skills by popularity, install/uninstall skills, inspect skill details, or search for specific functionality on ClawHub for Trae. This skill installs skills to .trae/skills by default and uses --agent trae with npx skills. Triggers on phrases like "search clawhub", "find skills", "browse skills", "popular skills", "best skills for", "install skill", "clawhub", "clawhub4trae", "trae clawhub", or when the user is looking for new agent capabilities for Trae. Always use this skill when the user mentions ClawHub or wants to search for AI agent skills for Trae.
---

# ClawHub4Trae CLI

Interact with ClawHub entirely via `npx clawhub` CLI, customized for Trae agents. This is the only reliable method — the ClawHub website uses Convex WebSocket for data loading, so WebFetch and direct browser URL navigation do not work for search.

## Default Configuration

- **Default install directory**: `.trae/skills`
- **Default agent flag**: `--agent trae` for `npx skills` commands

## Command Reference

### Search & Discover

```bash
# Vector search skills by keyword
npx clawhub search "<query>" [--limit <n>]

# Browse skills with sorting
npx clawhub explore [--sort <order>] [--limit <n>] [--json]
# sort options: newest, downloads, rating, installs, installsAllTime, trending
```

### Inspect Skills

```bash
# View skill metadata (name, author, description, version, tags, license)
npx clawhub inspect <slug> [--json]

# List all versions
npx clawhub inspect <slug> --versions [--limit <n>]

# List files in a skill
npx clawhub inspect <slug> --files

# Read a specific file's content (text files <= 200KB)
npx clawhub inspect <slug> --file <path>

# Inspect a specific version
npx clawhub inspect <slug> --version <version>
```

### Install & Manage (Trae-Specific)

```bash
# Install a skill to .trae/skills directory (only install command uses --dir)
npx clawhub install <slug> --dir .trae/skills

# Update installed skills (all or specific)
npx clawhub update [slug]

# Uninstall a skill
npx clawhub uninstall <slug>

# List installed skills
npx clawhub list

# Use npx skills with --agent trae flag (per user rules)
npx skills install <skill> --agent trae
```

### Publish & Sync

```bash
# Publish a skill from a folder
npx clawhub publish <path>

# Scan local skills dir and publish new/updated ones
npx clawhub sync
```

### Account & Auth

```bash
npx clawhub login        # Log in (opens browser or stores token)
npx clawhub logout       # Remove stored token
npx clawhub whoami       # Validate current token
```

### Other

```bash
npx clawhub star <slug>      # Favorite a skill
npx clawhub unstar <slug>    # Unfavorite
npx clawhub explore --json   # Get structured data for processing
```

## Workflow Guide

### When the user wants to search for skills

1. Run `npx clawhub search "<query>"` with appropriate keywords
2. Parse the output: each result shows slug, description, and relevance score
3. For top results, run `npx clawhub inspect <slug>` to get full details
4. Present results using the Recommendation Format below

### When the user wants to browse/explore skills

1. Determine the sort order based on user intent:
   - "most popular" / "top downloaded" → `--sort downloads`
   - "trending" / "hot right now" → `--sort trending`
   - "highest rated" / "best" → `--sort rating`
   - "most installed" → `--sort installs`
   - "newly published" / "latest" → `--sort newest`
   - No preference → `--sort trending` (good default for discovery)
2. Run `npx clawhub explore --sort <order> --limit <n>`
3. Present results

### When the user wants skill details

1. Run `npx clawhub inspect <slug>` for metadata
2. Run `npx clawhub inspect <slug> --files` to see file structure
3. If user wants to see specific content: `npx clawhub inspect <slug> --file SKILL.md`

### When the user wants to install a skill

1. First inspect to confirm it's the right one: `npx clawhub inspect <slug>`
2. Install with: `npx clawhub install <slug> --dir .trae/skills`
3. Confirm success
4. If using npx skills command, use: `npx skills install <skill> --agent trae` (per user rules)

### When the user wants to move an installed skill to .trae/skills

If a skill is already installed elsewhere, guide the user to:
1. Uninstall it from the current location
2. Reinstall it using `npx clawhub install <slug> --dir .trae/skills`

## Search Tips

- Use specific, narrow keywords: `"pdf edit"` not `"pdf"`
- Combine concepts: `"react testing"` not `"testing"`
- Search returns relevance scores — higher means better match
- For broad discovery, use `explore --sort trending` instead of search
- Use `--json` flag when you need to programmatically parse results

## Result Presentation

Evaluate each skill by relevance, popularity, community approval, maintenance status, and description clarity.

### Recommendation Format

```
🏆 Best match: <skill-name> by @<author>
   ⭐ <stars> · 📥 <downloads> · 📦 <installs>
   <one-line description>
   URL: https://clawhub.ai/<author>/<skill-name>

📋 Runner-up: <skill-name> by @<author>
   ⭐ <stars> · 📥 <downloads>
   <one-line description>
   URL: https://clawhub.ai/<author>/<skill-name>
```

## Important Notes

1. **Only `clawhub install` command uses `.trae/skills` directory** - update/uninstall/list/sync commands do not use --dir parameter
2. **Always use `--agent trae`** when using `npx skills` commands (per user rules)
3. **Ensure the `.trae/skills` directory exists** before installing - create it if necessary with `mkdir -p .trae/skills`
4. When instructing users to install skills, remind them that this skill uses the `.trae/skills` directory for install command only

## Why CLI Only

ClawHub's website (clawhub.ai) loads all skill data via Convex real-time database over WebSocket. This means:

- **WebFetch fails** — it only gets the empty initial HTML, no data
- **Direct browser URL navigation fails** — snapshotting before Convex finishes loading shows 0 results
- **Browser two-step works but is slow** — requires navigating, waiting 5-8 seconds for data sync, then typing in the search box

CLI calls the registry API directly and returns results instantly. Always prefer CLI.
