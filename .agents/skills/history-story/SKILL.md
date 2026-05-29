---
name: history-story
description: "Create historical stories from real events. Researches 'today in history' events, deep-dives into facts, applies D.E.S.I.R.E. Matrix analysis, then crafts immersive stories. Use when users ask to create historical stories, learn about 'today in history', adapt historical events into stories, or mention '历史故事', '历史上的今天', '写一个历史故事'."
---

# History Story

Turn historical events into immersive stories. 8-phase team pipeline with context isolation.

## Workflow

| Phase | Agent | Action | File |
|-------|-------|--------|------|
| 1 | Researcher | Fetch events (script + WebSearch) | `agents/researcher.md` |
| 2 | Researcher | Deep research (all events parallel) | `agents/researcher.md` |
| 3 | Analyst | D.E.S.I.R.E. Matrix analysis | `agents/analyst.md` |
| 4a | Evaluator | Event evaluation → eval-card.md | `agents/evaluator.md` |
| 4b | Selector | Pick 3-5 events (main agent, reads eval-cards only) | — |
| 4c | PitchEditor | Profile + pitch (selected events) | `agents/pitch-editor.md` |
| 5 | CharacterDesigner | Characters + relationships | `agents/character-designer.md` |
| 6 | Architect | Story outline | `agents/architect.md` |
| 7 | Storyteller | Write story | `agents/storyteller.md` |
| 8 | Editor | Fact-check review | `agents/editor.md` |

## Context Isolation

**Each sub-agent processes ONE event only, never cross-reads other events.** This prevents context explosion and cross-contamination. Only Selector reads across events (compact eval-cards only).

## Data Directories

- `./dayinhistory/{MM}/{DD}/` — raw event data + research
- `./history/{MM}/{DD}/` — creative output (matrix, profile, outline, story, review)

See `references/directory-structure.md` for full layout. Event slug format: `{year}-{name}` (e.g. `1945-广岛原子弹`).

## Data Acquisition

```bash
python scripts/fetch_history.py [--month M] [--day D] [--output OUTPUT]
```

Supplement with WebSearch: `历史上的今天 {M}月{D}日 重大事件`

## Reference Files

| Need | File |
|------|------|
| D.E.S.I.R.E. Matrix theory + WritingStyle derivation | `references/desire-matrix.md` |
| Directory structure detail | `references/directory-structure.md` |
| Selection template + criteria | `references/selection-template.md` |
| Parallel strategy | `references/parallel-strategy.md` |
