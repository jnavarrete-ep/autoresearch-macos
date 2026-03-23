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
