# autoskill

Autonomous evolution of Claude Code skills using the [autoresearch](https://github.com/karpathy/autoresearch) pattern.

## The Idea

Give an AI agent a skill and benchmarks, let it experiment autonomously. It modifies the skill, runs evaluations, checks if the result improved, keeps or discards, and repeats. You wake up to a log of experiments and a better skill.

Instead of evolving neural network training code to minimize loss, **autoskill evolves skill markdown files to maximize benchmark pass rates**.

## The Pattern

```
┌─────────────────────────────────────────────────┐
│                 AUTOSKILL LOOP                  │
├─────────────────────────────────────────────────┤
│  1. Modify skill.md                             │
│  2. git commit                                  │
│  3. uv run evaluate.py  → get pass_rate         │
│  4. If pass_rate ↑ → keep                       │
│     If pass_rate ↓ → git reset --hard HEAD~1    │
│  5. Log to results.tsv                          │
│  6. GOTO 1                                      │
└─────────────────────────────────────────────────┘
```

| Component | Purpose |
|-----------|---------|
| `skill.md` | The skill being evolved (agent modifies this) |
| `benchmarks/` | Test cases with expected behaviors (fixed) |
| `evaluate.py` | Runs skill against benchmarks via Claude CLI |
| `results.tsv` | Experiment history log |

## Included Skills

| Skill | Directory | Benchmarks | Best Score |
|-------|-----------|------------|------------|
| **Code Explainer** | `autoskill/` | 15 | 0.967 |
| **Commit Writer** | `autoskill-commit/` | 5 | 1.000 |
| **PR Reviewer** | `autoskill-review/` | 5 | 1.000 |
| **Multi-Model** | `autoskill-multimodel/` | 5 | 0.900 |

### Multi-Model Evaluation

`autoskill-multimodel/` uses [counselors](https://github.com/counselors-ai/counselors) to judge with multiple models in parallel:

```bash
# Uses claude-opus + codex-5.3-high by default
uv run autoskill-multimodel/evaluate.py

# Custom judges
JUDGE_TOOLS=claude-opus,claude-sonnet,codex-5.3-high uv run autoskill-multimodel/evaluate.py
```

Output shows per-model scores:
```
[PASS] 01_null_check_bug: 1.00 (34.7s) [claude-opus=1.0, codex-5.3-high=1.0]
```

Benefits: reduced variance, cross-model validation, bias detection.

## Quick Start

**Requirements:** Python 3.10+, [uv](https://docs.astral.sh/uv/), Claude CLI installed.

```bash
# Install dependencies
uv sync

# Run evaluation for any skill
uv run autoskill/evaluate.py
uv run autoskill-commit/evaluate.py
uv run autoskill-review/evaluate.py
```

## Running the Agent

Spin up Claude Code in this repo and prompt:

```
Read autoskill/program.md and start the autonomous skill evolution loop
```

The agent will iterate forever, trying modifications, keeping improvements, discarding failures.

## Creating Your Own Skill

1. Create a directory:
   ```
   my-skill/
   ├── skill.md           # The skill to evolve
   ├── evaluate.py        # Evaluation harness (copy from existing)
   ├── results.tsv        # Experiment log (start with header only)
   └── benchmarks/        # Test cases
       ├── 01_case.md
       └── 02_case.md
   ```

2. Each benchmark follows this format:
   ```markdown
   # Benchmark: Name

   ## Input
   [The input to give the skill]

   ## Expected Behaviors
   The output MUST:
   1. Do X
   2. Include Y
   3. NOT do Z

   ## Scoring
   - 1.0: All behaviors present
   - 0.5: Partial
   - 0.0: Failed
   ```

3. Let Claude iterate on `skill.md` until pass_rate plateaus.

## Key Learnings

From evolving these skills:

- **Specific beats generic**: "Use `fix:` for bugs with specific description" beats "write good messages"
- **Permission to approve**: "LGTM is valid for clean code" prevents over-criticism
- **Checklists work**: "Always mention X when present" improves consistency
- **LLM-as-judge has variance**: Run evaluations multiple times

## Design Principles

- **Single file to modify**: The agent only edits `skill.md`. Keeps scope manageable.
- **Fixed evaluation**: Benchmarks don't change during evolution. Fair comparison.
- **Git as checkpoint**: Commits mark progress, `reset --hard` reverts failures.
- **TSV as log**: Simple, appendable, diffable experiment history.

## Project Structure

```
autoskill/              — Code Explainer skill (15 benchmarks)
autoskill-commit/       — Commit Writer skill (5 benchmarks)
autoskill-review/       — PR Reviewer skill (5 benchmarks)
```

## Credits

Based on [@karpathy's autoresearch](https://github.com/karpathy/autoresearch) pattern for autonomous LLM training research.

## License

MIT
