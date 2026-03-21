# Benchmark: Race Condition Bug

## Input Code

```javascript
let balance = 100;

async function withdraw(amount) {
  if (balance >= amount) {
    await processPayment(amount);
    balance -= amount;
    return true;
  }
  return false;
}

// Called concurrently:
// withdraw(80);
// withdraw(80);
```

## Expected Behaviors

The explanation MUST:
1. Identify this as JavaScript
2. Explain it's a withdrawal function with balance check
3. **CRITICAL**: Identify the race condition (check-then-act bug)
4. Explain how concurrent calls can overdraw (both pass the check before either subtracts)
5. Suggest a fix (atomic operation, mutex, or transaction)

## Scoring

- 1.0: All 5 behaviors present (MUST include #3)
- 0.5: Identifies it's async but misses the race condition
- 0.0: Misses the concurrency bug entirely
