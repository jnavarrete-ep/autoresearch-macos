# Benchmark: Catastrophic Regex Backtracking

## Input Code

```python
import re

def validate_email(email):
    pattern = r'^([a-zA-Z0-9]+)+@([a-zA-Z0-9]+\.)+[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

# This hangs:
# validate_email('aaaaaaaaaaaaaaaaaaaaaaaaaaaa@')
```

## Expected Behaviors

The explanation MUST:
1. Identify this as Python
2. Explain it validates email format with regex
3. **CRITICAL**: Identify the catastrophic backtracking vulnerability (ReDoS)
4. Explain why: nested quantifiers `([a-zA-Z0-9]+)+` cause exponential backtracking
5. Note this is a denial-of-service risk with malicious input

## Scoring

- 1.0: All 5 behaviors present (MUST include #3)
- 0.5: Explains the regex but misses the ReDoS vulnerability
- 0.0: Misses the performance/security issue entirely
