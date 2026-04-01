# Benchmark: TypeError - Cannot read property of undefined

## Input Logs

```
TypeError: Cannot read property 'map' of undefined
    at Array.map (<anonymous>)
    at processUserList (/app/src/handlers/users.js:45:18)
    at async /app/src/handlers/users.js:32:5
    at Layer.handle [as handle_request] (/app/node_modules/express/lib/router/layer.js:95:5)

(node:12345) UnhandledPromiseRejectionWarning: This error originated either by throwing inside of an async function without a catch block, or by rejecting a promise which was not handled with .catch().
```

## Expected Behaviors

The analysis MUST:
1. Identify the error type as TypeError
2. Explain that `users.map` is called on undefined (data not loaded)
3. Pinpoint the location: users.js line 45
4. Explain the root cause: missing null check before mapping
5. Suggest a fix: add null check or optional chaining

## Scoring

- 1.0: All 5 behaviors present
- 0.5: Identifies error but misses root cause or fix
- 0.0: Misidentifies the error entirely
