#!/usr/bin/env bash
# harness-kit/init.sh — Initialize project workspace with OpenClaw harness files
# Usage: bash init.sh [target_dir]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REFS_DIR="${SCRIPT_DIR}/../references"
TARGET_DIR="${1:-.}"

TARGET_DIR="$(cd "$TARGET_DIR" 2>/dev/null && pwd)"
if [ -z "$TARGET_DIR" ]; then
  echo "Error: target directory '${1}' does not exist."
  exit 1
fi

if [ ! -d "$REFS_DIR" ]; then
  echo "Error: template directory '${REFS_DIR}' not found."
  exit 1
fi

created=0
skipped=0
linked=0

echo "harness-kit: initializing '${TARGET_DIR}'"
echo ""

for file in "$REFS_DIR"/*.md; do
  [ -f "$file" ] || continue
  filename="$(basename "$file")"
  target="${TARGET_DIR}/${filename}"

  if [ -f "$target" ]; then
    echo "  skip  ${filename} (already exists)"
    skipped=$((skipped + 1))
  else
    cp "$file" "$target"
    echo "  create ${filename}"
    created=$((created + 1))
  fi
done

TRAE_RULES_DIR="${TARGET_DIR}/.trae/rules"
AGENTS_SRC="${TARGET_DIR}/AGENTS.md"
AGENTS_LINK="${TRAE_RULES_DIR}/AGENTS.md"

if [ -f "$AGENTS_SRC" ]; then
  mkdir -p "$TRAE_RULES_DIR"
  if [ -L "$AGENTS_LINK" ]; then
    existing_target="$(readlink -f "$AGENTS_LINK" 2>/dev/null || true)"
    if [ "$existing_target" = "$(readlink -f "$AGENTS_SRC")" ] || [ "$existing_target" = "$AGENTS_SRC" ]; then
      echo "  skip  .trae/rules/AGENTS.md (symlink already correct)"
    else
      rm -f "$AGENTS_LINK"
      ln -s "$AGENTS_SRC" "$AGENTS_LINK"
      echo "  fix   .trae/rules/AGENTS.md (symlink updated)"
    fi
  elif [ -f "$AGENTS_LINK" ]; then
    echo "  skip  .trae/rules/AGENTS.md (regular file exists, not overwriting)"
  else
    ln -s "$AGENTS_SRC" "$AGENTS_LINK"
    echo "  link  .trae/rules/AGENTS.md -> AGENTS.md"
    linked=$((linked + 1))
  fi
fi

echo ""
echo "Done: ${created} created, ${skipped} skipped, ${linked} linked."
