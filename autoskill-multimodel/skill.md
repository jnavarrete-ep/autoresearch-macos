---
name: code-explainer-v2
description: Explains what code does with multi-model validated quality
version: 0.1.0
---

# Code Explainer

Takes code as input and produces a clear, accurate explanation.

## Instructions

When given code to explain:

1. **Identify the language** and any frameworks/libraries used
2. **State the purpose** in one sentence
3. **Walk through the logic** step by step
4. **Note any issues** (bugs, security, performance)
5. **Summarize** what a caller/user would experience

## Output Format

```
## Language
[language name]

## Purpose
[one sentence summary]

## How It Works
[step-by-step explanation]

## Issues
[bugs, security concerns, or "None identified"]

## Summary
[what the user experiences]
```

## Rules

- Be accurate — describe what the code does, not what comments say
- Be specific — reference exact lines and values
- Flag problems — always mention bugs and security issues
- List ALL issues found, not just the first one
- If code is clean and correct, say "None identified" in Issues section

## Common Bug Patterns

For loops: check both termination condition AND bounds access. If a loop accesses arr[i] without checking i < len(arr), it can cause IndexError. If the loop condition might never be false, it can cause infinite loops. If a loop searches for something and the target might not exist, note the infinite loop risk. Mention all risks and suggest fixes (bounds check, enumerate, try/catch).

For async: check for race conditions (read-modify-write patterns where concurrent calls can interleave). Explain HOW the race occurs and suggest fixes (atomic ops, locks, transactions).

For property access: check for null/undefined at each level of the chain. If user.profile.name is accessed without checks, flag that user, user.profile, or user.profile.name could be null/undefined causing TypeError. Suggest optional chaining (user?.profile?.name) or explicit null checks.

## What Counts as an Issue

Real issues to flag:
- Code that can crash (null access, out of bounds, division by zero)
- Security vulnerabilities (injection, path traversal)
- Race conditions that cause incorrect results
- Infinite loops or hangs

NOT issues (don't flag these):
- Style preferences
- Missing features the code wasn't designed for
- Theoretical edge cases that are clearly outside intended use
