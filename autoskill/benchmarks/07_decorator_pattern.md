# Benchmark: Python Decorator with Arguments

## Input Code

```python
def retry(max_attempts=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)
            return wrapper
        return decorator

@retry(max_attempts=5, delay=2)
def fetch_data(url):
    return requests.get(url).json()
```

## Expected Behaviors

The explanation MUST:
1. Identify this as Python
2. Identify it as a decorator factory (decorator that takes arguments)
3. Explain the retry logic (attempts, delay between retries)
4. Note that it preserves function metadata (functools.wraps)
5. Explain when the exception is re-raised (after all attempts exhausted)

## Scoring

- 1.0: All 5 behaviors present
- 0.5: 3-4 behaviors present
- 0.0: 2 or fewer behaviors present
