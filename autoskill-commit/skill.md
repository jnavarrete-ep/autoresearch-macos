---
name: commit-writer
description: Generates concise, meaningful git commit messages from diffs
version: 0.1.0
---

# Commit Message Writer

Takes a git diff and produces a commit message following best practices.

## Instructions

When given a diff:

1. Identify what changed (files, functions, logic)
2. Determine the type of change (feat, fix, refactor, docs, test, chore)
3. Write a concise subject line (max 50 chars)
4. Add body if needed (wrap at 72 chars)

## Output Format

```
<type>: <subject>

[optional body]
```

## Rules

- Subject: imperative mood ("Add feature" not "Added feature")
- Subject: no period at the end
- Subject: max 50 characters
- Body: explain what and why, not how

## Type Guidelines

- **fix**: Bug fixes. Be specific: "fix null check in calculateTotal" not "fix bug"
- **feat**: New functionality. Focus on user value, not implementation
- **refactor**: Code changes that don't affect behavior
- **feat!** or **BREAKING CHANGE**: When API/behavior changes incompatibly. Always include migration notes in body
