# Benchmark: Null Check Bug

## Input Code

```javascript
function getUserName(user) {
  return user.profile.name.toUpperCase();
}
```

## Expected Behaviors

The explanation MUST:
1. Identify this as JavaScript
2. Explain it gets the uppercase name from a user's profile
3. **CRITICAL**: Identify the null/undefined risk (no null checks)
4. Note that user, profile, or name could be undefined
5. Suggest optional chaining or null checks

## Scoring

- 1.0: All 5 behaviors present (MUST include #3)
- 0.5: Explains function but misses the null safety issue
- 0.0: Misses the bug entirely
