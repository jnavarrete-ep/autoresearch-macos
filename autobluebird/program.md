# autobluebird

Autonomous false-positive reduction for Bluebird NestJS diagnostics using the autoresearch pattern.

## Concept

Instead of evolving neural network training code (`train.py`), we evolve the Bluebird cross-validation layer and rule heuristics. Instead of measuring `val_bpb`, we measure a **calibrated objective score** that rewards high true-positive rates and penalizes false positives.

## Setup

1. **Agree on a run tag**: propose a tag based on today's date (e.g. `mar20`). Branch `autobluebird/<tag>` must not exist.
2. **Create the branch**: `git checkout -b autobluebird/<tag>` from current HEAD.
3. **Read the files**:
   - `autobluebird/manifest.json` — benchmark project paths and options (EDIT paths, DO NOT change schema)
   - `autobluebird/evaluate.py` — evaluation harness (DO NOT EDIT)
   - The Bluebird source at the path configured in your environment
4. **Configure manifest.json**: Set the `path` field for each project entry to an absolute path to a NestJS project on this machine.
5. **Initialize results.tsv**: Create `autobluebird/results.tsv` with just the header row.
6. **Confirm and go**.

## The Files Under Evolution

You modify the Bluebird cross-validation and rule logic to reduce false positives. The key files you can edit are in the Bluebird repo:

- `packages/bluebird/src/utils/cross-validate.ts` — the cross-validation layer with heuristic refuters
- `packages/bluebird/src/rules/*.ts` — individual rule checker implementations
- `packages/bluebird/src/rules/checkers.ts` — rule-to-checker mappings
- `packages/bluebird/src/rules/index.ts` — rule metadata and enablement predicates

**DO NOT EDIT**: `evaluate.py`, `manifest.json` schema, `calculate-score.ts`, `orchestrate.ts`, `types.ts`.

## Evaluation

```bash
uv run autobluebird/evaluate.py > eval.log 2>&1
```

Output format:
```
---
objective:              85.500
raw_score_avg:          80.000
calibrated_score_avg:   88.000
estimated_fp_rate:      0.0500
projects_evaluated:     3
avg_time_sec:           12.3
```

Extract the metric:
```bash
grep "^objective:" eval.log
```

## Logging Results

Log to `autobluebird/results.tsv` (tab-separated):

```
commit	objective	raw_score_avg	calibrated_score_avg	estimated_fp_rate	status	description
```

- commit: git hash (7 chars)
- objective: the combined metric (higher is better)
- raw_score_avg: average raw Bluebird score across benchmark projects
- calibrated_score_avg: average calibrated score (excludes likely false positives)
- estimated_fp_rate: fraction of diagnostics classified as likely false positive
- status: `keep`, `discard`, or `crash`
- description: what you tried

Example:
```
commit	objective	raw_score_avg	calibrated_score_avg	estimated_fp_rate	status	description
a1b2c3d	85.500	80.000	88.000	0.0500	keep	baseline
b2c3d4e	87.200	80.000	89.500	0.0460	keep	tighten missing-caching refuter for small projects
c3d4e5f	84.100	80.000	86.000	0.0380	discard	overly aggressive FP filtering on security rules
```

## The Experiment Loop

LOOP FOREVER:

1. Read current cross-validation logic and recent results
2. Propose a modification to reduce false positives:
   - Add or refine a heuristic refuter in `cross-validate.ts`
   - Tighten a rule checker's predicate to avoid false matches
   - Add an `enabledWhen` gate based on project features
   - Adjust confidence thresholds
3. Make the edit in the Bluebird source
4. Rebuild Bluebird: `cd <bluebird-path> && npm run build`
5. git commit (in autoresearch repo)
6. Run: `uv run autobluebird/evaluate.py > eval.log 2>&1`
7. Extract: `grep "^objective:" eval.log`
8. If empty, it crashed — `tail -50 eval.log` to debug
9. Log to results.tsv
10. If objective improved (higher): keep commit
11. If equal or worse: `git reset --hard HEAD~1` and try different idea

## Modification Ideas

- Add project-metadata-aware refuters for heuristic rules
- Use source file count thresholds to skip irrelevant rules for tiny projects
- Use ORM detection to skip database rules when no ORM is present
- Use feature detection (swagger, graphql, microservices) to gate rules
- Tighten regex/AST patterns in rule checkers to reduce noise
- Add path-based exclusions for known non-application files
- Remove overly aggressive rules that have high FP rates

## Simplicity Criterion

All else equal, simpler is better:
- +2.0 objective with a clean refuter? Definitely keep
- +0.1 objective with 20 lines of complex logic? Probably discard
- Equal objective with fewer lines? Definitely keep
- Removing a noisy rule entirely and improving objective? Keep

## NEVER STOP

Once the loop begins, do NOT pause to ask if you should continue. Run until manually interrupted. If stuck, try more radical changes or revisit discarded ideas with tweaks.
