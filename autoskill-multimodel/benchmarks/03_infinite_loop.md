# Benchmark: Infinite Loop Risk

## Input Code

```python
def find_element(arr, target):
    i = 0
    while arr[i] != target:
        i += 1
    return i
```

## Expected Behaviors

The explanation MUST:
1. Identify this as Python
2. Explain it searches for target in array
3. **CRITICAL**: Identify infinite loop risk if target not found
4. Note potential IndexError when i exceeds array length
5. Suggest bounds checking or using enumerate/index()

## Scoring

- 1.0: All 5 behaviors present (MUST include #3 and #4)
- 0.5: Mentions one issue but not both
- 0.0: Misses the bugs
