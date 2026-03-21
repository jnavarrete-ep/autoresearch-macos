# Benchmark: Goroutine Leak

## Input Code

```go
func fetchWithTimeout(url string, timeout time.Duration) ([]byte, error) {
    ch := make(chan []byte)

    go func() {
        resp, err := http.Get(url)
        if err != nil {
            return
        }
        defer resp.Body.Close()
        body, _ := io.ReadAll(resp.Body)
        ch <- body
    }()

    select {
    case data := <-ch:
        return data, nil
    case <-time.After(timeout):
        return nil, errors.New("timeout")
    }
}
```

## Expected Behaviors

The explanation MUST:
1. Identify this as Go
2. Explain it fetches a URL with a timeout using goroutines and channels
3. **CRITICAL**: Identify the goroutine leak when timeout occurs
4. Explain why: the goroutine blocks forever on `ch <- body` because no one is receiving after timeout
5. Suggest fix: use buffered channel `make(chan []byte, 1)` or context cancellation

## Scoring

- 1.0: All 5 behaviors present (MUST include #3)
- 0.5: Explains the timeout pattern but misses the goroutine leak
- 0.0: Misses the leak entirely
