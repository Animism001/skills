#!/usr/bin/env python3
"""Skill audit script — measures token budget, description quality, and structure health."""

import os
import re
import sys
import json
import math
from pathlib import Path

SKILLS_DIR = sys.argv[1] if len(sys.argv) > 1 else "."
BUDGET_PERCENT = 2
CONTEXT_TOKENS = 200000
CHARS_PER_TOKEN = 4

def token_cost(text):
    return math.ceil(len(text.encode("utf-8")) / CHARS_PER_TOKEN)

def parse_frontmatter(content):
    if not content.startswith("---"):
        return None, content
    end = content.find("\n---", 3)
    if end == -1:
        return None, content
    fm_text = content[3:end].strip()
    body = content[end + 4:].strip()
    fm = {}
    current_key = None
    for line in fm_text.split("\n"):
        if ":" in line and not line.startswith(" ") and not line.startswith("\t"):
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if val == "|":
                current_key = key
                fm[key] = ""
            else:
                current_key = None
                fm[key] = val.strip('"').strip("'")
        elif current_key and (line.startswith("  ") or line.startswith("\t")):
            fm[current_key] += line.strip() + " "
    for k in fm:
        if isinstance(fm[k], str):
            fm[k] = fm[k].strip()
    return fm, body

def count_words(text):
    return len(text.split())

def audit_skill(skill_dir):
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return None

    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    fm, body = parse_frontmatter(content)
    lines = content.split("\n")
    line_count = len(lines)
    byte_count = len(content.encode("utf-8"))
    token_count = token_cost(content)

    name = fm.get("name", "") if fm else ""
    desc = fm.get("description", "") if fm else ""
    desc_words = count_words(desc)
    desc_chars = len(desc)

    rendered_line = f"- {name}: {desc} (file: {skill_md})" if desc else f"- {name}: (file: {skill_md})"
    rendered_tokens = token_cost(rendered_line + "\n")

    has_refs = os.path.isdir(os.path.join(skill_dir, "references"))
    has_scripts = os.path.isdir(os.path.join(skill_dir, "scripts"))
    has_agents = os.path.isdir(os.path.join(skill_dir, "agents"))

    ref_count = 0
    if has_refs:
        for root, dirs, files in os.walk(os.path.join(skill_dir, "references")):
            ref_count += len([f for f in files if f.endswith(".md")])

    script_count = 0
    if has_scripts:
        for root, dirs, files in os.walk(os.path.join(skill_dir, "scripts")):
            script_count += len([f for f in files if f.endswith((".py", ".ts", ".js", ".sh"))])

    agent_count = 0
    if has_agents:
        for root, dirs, files in os.walk(os.path.join(skill_dir, "agents")):
            agent_count += len([f for f in files if f.endswith(".md")])

    body_lines = body.split("\n") if body else []
    body_line_count = len(body_lines)

    sections = re.findall(r"^##\s+(.+)$", content, re.MULTILINE)
    section_count = len(sections)

    issues = []
    if fm is None:
        issues.append("no_frontmatter")
    if line_count > 500:
        issues.append(f"over_500_lines({line_count})")
    if line_count > 200:
        issues.append(f"over_200_lines({line_count})")
    if desc_words > 40:
        issues.append(f"desc_over_40_words({desc_words})")
    if desc_words > 80:
        issues.append(f"desc_over_80_words({desc_words})")
    if not has_refs and line_count > 100:
        issues.append("no_refs_but_long_skillmd")
    if not has_scripts and line_count > 100:
        issues.append("no_scripts_but_long_skillmd")

    score = 100
    if fm is None:
        score -= 30
    if line_count > 500:
        score -= 20
    elif line_count > 200:
        score -= 10
    if desc_words > 80:
        score -= 15
    elif desc_words > 40:
        score -= 5
    if not has_refs and line_count > 100:
        score -= 10
    if not has_scripts and line_count > 100:
        score -= 5

    return {
        "name": name or os.path.basename(skill_dir),
        "line_count": line_count,
        "body_line_count": body_line_count,
        "byte_count": byte_count,
        "token_count": token_count,
        "rendered_tokens": rendered_tokens,
        "desc_words": desc_words,
        "desc_chars": desc_chars,
        "section_count": section_count,
        "has_refs": has_refs,
        "has_scripts": has_scripts,
        "has_agents": has_agents,
        "ref_count": ref_count,
        "script_count": script_count,
        "agent_count": agent_count,
        "issues": issues,
        "health_score": max(0, score),
    }

def main():
    skills = []
    for entry in sorted(os.listdir(SKILLS_DIR)):
        skill_dir = os.path.join(SKILLS_DIR, entry)
        if os.path.isdir(skill_dir) and os.path.isfile(os.path.join(skill_dir, "SKILL.md")):
            result = audit_skill(skill_dir)
            if result:
                skills.append(result)

    budget_tokens = int(CONTEXT_TOKENS * BUDGET_PERCENT / 100)
    total_rendered = sum(s["rendered_tokens"] for s in skills)
    total_skillmd = sum(s["token_count"] for s in skills)

    print(f"# Skill Audit Report")
    print(f"generated: {__import__('datetime').datetime.now().isoformat()}")
    print(f"context_tokens: {CONTEXT_TOKENS}")
    print(f"budget_{BUDGET_PERCENT}%: {budget_tokens} tokens")
    print(f"cost_rule: ceil(utf8_bytes / {CHARS_PER_TOKEN})")
    print(f"skills_audited: {len(skills)}")
    print(f"total_rendered_tokens: {total_rendered}")
    print(f"total_skillmd_tokens: {total_skillmd}")
    print(f"budget_used: {total_rendered / budget_tokens * 100:.1f}%")
    print()

    print("## Per-Skill Metrics")
    print(f"| Skill | Lines | Tokens | Desc Words | Rendered Tok | Refs | Scripts | Agents | Score | Issues |")
    print(f"|-------|-------|--------|------------|-------------|------|---------|--------|-------|--------|")
    for s in skills:
        issues_str = ", ".join(s["issues"]) if s["issues"] else "✅"
        print(f"| {s['name']} | {s['line_count']} | {s['token_count']} | {s['desc_words']} | {s['rendered_tokens']} | {s['ref_count']} | {s['script_count']} | {s['agent_count']} | {s['health_score']} | {issues_str} |")

    print()

    target_skills = ["novel-analysis", "huashu-nuwa", "history-story", "expert-panel", "concept-builder", "matrix-web"]
    print("## Target Skills Detail (for before/after comparison)")
    target_data = [s for s in skills if s["name"] in target_skills or os.path.basename(next((d for d in os.listdir(SKILLS_DIR) if os.path.isfile(os.path.join(SKILLS_DIR, d, "SKILL.md")) and audit_skill(os.path.join(SKILLS_DIR, d)) and audit_skill(os.path.join(SKILLS_DIR, d))["name"] == s["name"]), "")) in target_skills]
    target_data = [s for s in skills if any(t in s["name"] for t in target_skills)]

    json_output = {
        "meta": {
            "context_tokens": CONTEXT_TOKENS,
            "budget_percent": BUDGET_PERCENT,
            "budget_tokens": budget_tokens,
            "cost_rule": f"ceil(utf8_bytes / {CHARS_PER_TOKEN})",
        },
        "skills": {s["name"]: s for s in skills},
        "targets": {s["name"]: s for s in skills if any(t in s["name"] for t in target_skills)},
    }

    out_path = os.path.join(os.path.dirname(SKILLS_DIR) or ".", "skill-audit-baseline.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(json_output, f, ensure_ascii=False, indent=2)
    print(f"Baseline saved to: {out_path}")

if __name__ == "__main__":
    main()
