---
name: log-analyzer
description: Analyzes error logs and stack traces to identify root causes and suggest fixes
version: 0.1.0
---

# Log Analyzer

Takes error logs or stack traces as input and produces a clear analysis of the problem.

## Instructions

When given logs to analyze:

1. **Identify the error type** (Error, Warning, Exception, etc.)
2. **Extract the root cause** from the stack trace or error message
3. **Determine the affected component** (service, function, line number)
4. **Explain what went wrong** in plain language
5. **Suggest actionable fixes**

## Output Format

```
## Error Type
[type]

## Root Cause
[one sentence summary of what failed]

## Affected Component
[service/file/function @ line X]

## Explanation
[plain language explanation of the error chain]

## Suggested Fix
[actionable steps to resolve the issue]
```

## Error Patterns to Recognize

### JavaScript/Node.js
- `ReferenceError`: Variable not defined
- `TypeError`: Wrong type used (e.g., calling non-function)
- `SyntaxError`: Parse error
- `Promise rejections`: Unhandled async errors

### Python
- `TypeError`, `ValueError`, `KeyError`, `IndexError`: Common Python exceptions
- `ImportError`, `ModuleNotFoundError`: Missing dependencies
- `AttributeError`: Object doesn't have that attribute

### Network Errors
- `ECONNREFUSED`: Service not running
- `ETIMEDOUT`: Request timeout
- `ENOTFOUND`: DNS resolution failed

### Database Errors
- `connection refused`: Database not accessible
- `deadlock`: Concurrent transaction conflict
- `syntax error`: SQL query malformed

## Rules

- Focus on the FIRST error in a stack trace (often the root cause)
- Ignore noise like internal framework logs
- Be specific about line numbers and function names
- Provide actionable fixes, not generic advice
- If multiple errors exist, prioritize by severity
