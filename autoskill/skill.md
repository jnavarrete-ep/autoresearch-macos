---
name: code-explainer
description: Explains what a piece of code does in plain language
version: 0.1.0
---

# Code Explainer

Takes code as input and produces a clear, accurate explanation.

## Instructions

When given code to explain:

1. **Identify the language** and any frameworks/libraries used
2. **State the purpose** in one sentence
3. **Walk through the logic** step by step, noting:
   - Control flow (conditions, loops, recursion)
   - Side effects (API calls, state changes, cleanup/teardown)
   - Dependencies and parameters that affect behavior
4. **Note any edge cases** or potential issues (including security concerns)
5. **Summarize** what a caller/user would experience

## Output Format

```
## Language
[language name]

## Purpose
[one sentence summary]

## How It Works
[step-by-step explanation]

## Edge Cases
[potential issues or gotchas]

## Summary
[what the user experiences]
```

## Constraints

- Be accurate — don't guess at behavior you're unsure of
- Be concise — no unnecessary words
- Use plain language — avoid jargon unless explaining it

## Always Mention When Present

- Framework patterns: hooks, decorators, middleware, observers
- Timing patterns: debouncing, throttling, polling, retries
- Resource management: cleanup functions, disposal, unsubscribe
- Configuration: dependency arrays, options objects, defaults

## Critical Rules

1. **Read the code, not the comments** — Comments can be wrong or misleading. Always describe what the code actually does.
2. **Recognize patterns through obfuscation** — If code implements a known algorithm (FizzBuzz, sorting, etc.), identify it even if minified.
3. **Flag language-specific traps**:
   - JavaScript: type coercion with ==, string vs number comparisons, truthy/falsy
   - Python: mutable default arguments, late binding closures
   - Go: nil interface vs nil pointer, goroutine leaks
