# Benchmark: SQL Injection

## Input Code

```python
def search_users(query):
    sql = f"SELECT * FROM users WHERE name LIKE '%{query}%'"
    return db.execute(sql)
```

## Expected Behaviors

The explanation MUST:
1. Identify this as Python
2. Explain it searches users by name pattern
3. **CRITICAL**: Identify SQL injection vulnerability
4. Explain the attack vector (user input in query string)
5. Suggest parameterized queries as fix

## Scoring

- 1.0: All 5 behaviors present (MUST include #3)
- 0.5: Explains function but weak on security
- 0.0: Misses SQL injection entirely
