# Benchmark: Python KeyError

## Input Logs

```
Traceback (most recent call last):
  File "/app/api/views.py", line 142, in get_user
    user = db.query(User).filter_by(id=user_id).first()
  File "/app/db.py", line 89, in query
    return self.session.execute(stmt)
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/orm/session.py", line 1648, in execute
    raise exc.StaleDataError("Statement "
sqlalchemy.exc.StaleDataError: UPDATE statement on table 'users' expected to update 1 row(s). Affected: 0
```

## Expected Behaviors

The analysis MUST:
1. Identify error type as StaleDataError from SQLAlchemy
2. Explain root cause: UPDATE expected to modify 1 row but found 0 (user was deleted or doesn't exist)
3. Pinpoint: query.py line 142 handling get_user
4. Explain: race condition or user was deleted between check and update
5. Suggest fix: check if user exists before update, or handle 0 rows affected

## Scoring

- 1.0: All 5 behaviors present
- 0.5: Identifies database error but misses race condition aspect
- 0.0: Misidentifies the error
