#!/usr/bin/env bash
# harness-kit/init.sh — Initialize project workspace with OpenClaw harness files
# Usage: bash init.sh [--type <default|claude|trae>] [target_dir]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REFS_DIR="${SCRIPT_DIR}/../references"

# Parse arguments
TYPE="default"
TARGET_DIR="."

while [[ $# -gt 0 ]]; do
  case $1 in
    --type)
      TYPE="${2:-default}"
      shift 2
      ;;
    --type=*)
      TYPE="${1#*=}"
      shift
      ;;
    -h|--help)
      echo "Usage: bash init.sh [--type <default|claude|trae>] [target_dir]"
      echo ""
      echo "Types:"
      echo "  default  - .agents/{skills,rules,workflows}/ + root-level MD files"
      echo "  claude   - same as default, plus CLAUDE.md (@AGENTS.md) + .claude/ -> .agents/"
      echo "  trae     - same as default, plus .trae/ with subdir symlinks:"
      echo "             .trae/{skills,rules,workflows} -> .agents/"
      exit 0
      ;;
    *)
      TARGET_DIR="$1"
      shift
      ;;
  esac
done

# Validate type
case $TYPE in
  default|claude|trae) ;;
  *)
    echo "Error: unknown type '$TYPE'. Use: default, claude, or trae."
    exit 1
    ;;
esac

# Resolve target to absolute path
TARGET_DIR="$(cd "$TARGET_DIR" 2>/dev/null && pwd)" || {
  echo "Error: target directory does not exist."
  exit 1
}

if [ ! -d "$REFS_DIR" ]; then
  echo "Error: template directory '${REFS_DIR}' not found."
  exit 1
fi

created=0
skipped=0

echo "harness-kit: initializing '${TARGET_DIR}' (type: ${TYPE})"
echo ""

# ============================================================
# Step 1: Create .agents/ directory with subdirectories (all types)
# ============================================================
AGENTS_DIR="${TARGET_DIR}/.agents"
if [ -d "$AGENTS_DIR" ]; then
  echo "  skip  .agents/ (already exists)"
  skipped=$((skipped + 1))
else
  mkdir -p "$AGENTS_DIR"
  echo "  create .agents/"
  created=$((created + 1))
fi

# Create subdirectories inside .agents/
for subdir in skills rules workflows; do
  src="${REFS_DIR}/${subdir}"
  dest="${AGENTS_DIR}/${subdir}"
  if [ -d "$src" ]; then
    if [ -d "$dest" ]; then
      echo "  skip  .agents/${subdir}/ (already exists)"
      skipped=$((skipped + 1))
    else
      mkdir -p "$dest"
      if [ -n "$(ls -A "$src" 2>/dev/null)" ]; then
        cp -r "$src"/* "$dest"/
        echo "  create .agents/${subdir}/ (with files)"
      else
        echo "  create .agents/${subdir}/"
      fi
      created=$((created + 1))
    fi
  fi
done

# ============================================================
# Step 2: Copy/release MD files to project root (ALL types)
# ============================================================
for file in "$REFS_DIR"/*.md; do
  [ -f "$file" ] || continue
  filename="$(basename "$file")"

  dest="${TARGET_DIR}/${filename}"
  if [ -f "$dest" ] || [ -L "$dest" ]; then
    echo "  skip  ${filename} (already exists)"
    skipped=$((skipped + 1))
  else
    cp "$file" "$dest"
    echo "  create ${filename}"
    created=$((created + 1))
  fi
done

# ============================================================
# Step 3: Type-specific extras
# ============================================================

if [ "$TYPE" = "claude" ]; then
  # --- Claude: create CLAUDE.md (@AGENTS.md) + .claude/ -> .agents/ ---

  # Create CLAUDE.md in project root
  claude_md="${TARGET_DIR}/CLAUDE.md"
  if [ -f "$claude_md" ] || [ -L "$claude_md" ]; then
    echo "  skip  CLAUDE.md (already exists)"
    skipped=$((skipped + 1))
  else
    echo "@AGENTS.md" > "$claude_md"
    echo "  create CLAUDE.md"
    created=$((created + 1))
  fi

  # Create .claude/ -> .agents/ symlink
  claude_link="${TARGET_DIR}/.claude"
  if [ -L "$claude_link" ]; then
    echo "  skip  .claude -> .agents (symlink already exists)"
    skipped=$((skipped + 1))
  elif [ -e "$claude_link" ]; then
    echo "  skip  .claude (exists and is not a symlink, remove it first)"
    skipped=$((skipped + 1))
  else
    ln -s ".agents" "$claude_link"
    echo "  create .claude -> .agents"
    created=$((created + 1))
  fi

elif [ "$TYPE" = "trae" ]; then
  # --- Trae: .trae/ contains ONLY symlinks, no real files ---
  trae_dir="${TARGET_DIR}/.trae"
  if [ -d "$trae_dir" ]; then
    echo "  skip  .trae/ (already exists)"
    skipped=$((skipped + 1))
  else
    mkdir -p "$trae_dir"
    echo "  create .trae/"
    created=$((created + 1))
  fi

  # Create .trae/ subdirectory symlinks -> .agents/
  for subdir in skills rules workflows; do
    link="${trae_dir}/${subdir}"
    if [ -L "$link" ]; then
      echo "  skip  .trae/${subdir} -> .agents/${subdir} (symlink already exists)"
      skipped=$((skipped + 1))
    elif [ -e "$link" ]; then
      echo "  skip  .trae/${subdir} (exists and is not a symlink, remove it first)"
      skipped=$((skipped + 1))
    else
      ln -s "../.agents/${subdir}" "$link"
      echo "  create .trae/${subdir} -> .agents/${subdir}"
      created=$((created + 1))
    fi
  done

fi

echo ""
echo "Done: ${created} created, ${skipped} skipped."
