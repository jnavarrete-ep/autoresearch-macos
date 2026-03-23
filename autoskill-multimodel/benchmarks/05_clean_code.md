# Benchmark: Clean Code (Don't Over-Criticize)

## Input Code

```typescript
function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}
```

## Expected Behaviors

The explanation MUST:
1. Identify this as TypeScript
2. Explain it constrains a value between min and max
3. Recognize this is clean, correct, idiomatic code
4. NOT invent problems that don't exist
5. Issues section should say "None identified" or similar

## Scoring

- 1.0: Correctly approves without inventing issues
- 0.5: Mostly correct but adds unnecessary concerns
- 0.0: Invents bugs or security issues that don't exist
