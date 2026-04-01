# Benchmark: SQL Syntax Error

## Input Logs

```
org.postgresql.util.PSQLException: ERROR: syntax error at or near "SELEC"
  Position: 8
    at org.postgresql.core.v3.QueryExecutorImpl.receiveErrorResponse(QueryExecutorImpl.java:2557)
    at org.postgresql.core.v3.QueryExecutorImpl.handleCommandStatus(QueryExecutorImpl.java:2314)
    at org.postgresql.core.v3.QueryExecutorImpl.processResults(QueryExecutorImpl.java:1448)
    at org.postgresql.core.v3.QueryExecutorImpl.execute(QueryExecutorImpl.java:678)
    at com.zaxxer.hikari.pool.ProxyPreparedStatement.execute(ProxyPreparedStatement.java:62)
    at com.zaxxer.hikari.pool.HikariPooledStatement.execute(HikariPooledStatement.java:77)
    at dao.UserDAO.findByEmail(UserDAO.java:34)

Query: SELEC * FROM users WHERE email = $1
```

## Expected Behaviors

The analysis MUST:
1. Identify as PSQLException - SQL syntax error
2. Explain root cause: "SELEC" is typo, should be "SELECT"
3. Pinpoint: UserDAO.java line 34
4. Note: typo in SQL query string
5. Suggest fix: Change "SELEC" to "SELECT" in the query

## Scoring

- 1.0: All 5 behaviors present
- 0.5: Identifies syntax error but misses the typo detail
- 0.0: Misidentifies as Java error
