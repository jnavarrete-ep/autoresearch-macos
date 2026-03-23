# Benchmark: Race Condition

## Input Code

```javascript
let counter = 0;

async function incrementCounter() {
  const current = counter;
  await saveToDatabase(current + 1);
  counter = current + 1;
}
```

## Expected Behaviors

The explanation MUST:
1. Identify this as JavaScript
2. Explain it increments a counter and saves to database
3. **CRITICAL**: Identify the race condition
4. Explain how concurrent calls read same value before either writes
5. Suggest atomic operations or locking

## Scoring

- 1.0: All 5 behaviors present (MUST include #3)
- 0.5: Mentions async but misses race condition
- 0.0: Treats code as correct
