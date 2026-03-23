# autoskill-multimodel

Multi-model evaluation for skill evolution using [counselors](https://github.com/counselors-ai/counselors).

## What's Different

Instead of a single LLM judging skill outputs, **multiple models judge in parallel** and scores are aggregated. This reduces variance and bias from any single model.

```
┌─────────────────────────────────────────────────┐
│            MULTI-MODEL EVALUATION               │
├─────────────────────────────────────────────────┤
│  1. Run skill (Claude)                          │
│  2. Judge output with counselors:               │
│     ├── Claude Opus   → score                   │
│     ├── Codex 5.3     → score                   │
│     └── [other models] → score                  │
│  3. Aggregate scores (median)                   │
│  4. Keep/discard based on aggregated score      │
└─────────────────────────────────────────────────┘
```

## Setup

1. Install counselors: `npm install -g counselors`
2. Configure models: `counselors init --auto`
3. Set judge tools (optional): `export JUDGE_TOOLS=claude-opus,codex-5.3-high`

## Running

```bash
# Default judges (claude-opus, codex-5.3-high)
uv run evaluate.py

# Custom judges
JUDGE_TOOLS=claude-opus,claude-sonnet,codex-5.3-high uv run evaluate.py
```

## The Evolution Loop

Same as standard autoskill, but with more robust scoring:

1. Modify `skill.md`
2. `git commit`
3. `uv run evaluate.py` → multi-model pass_rate
4. If improved → keep, else → `git reset --hard HEAD~1`
5. Log to `results.tsv`
6. Repeat

## Benefits

- **Reduced variance**: Multiple models smooth out single-model quirks
- **Cross-model validation**: If Claude and Codex both flag an issue, it's real
- **Bias detection**: Disagreement between models reveals ambiguous criteria
