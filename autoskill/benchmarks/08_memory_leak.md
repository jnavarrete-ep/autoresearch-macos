# Benchmark: Memory Leak in Event Listener

## Input Code

```javascript
class DataFetcher {
  constructor(url) {
    this.url = url;
    this.data = null;

    window.addEventListener('online', () => {
      this.refresh();
    });
  }

  async refresh() {
    this.data = await fetch(this.url).then(r => r.json());
  }

  getData() {
    return this.data;
  }
}

// Usage: instances created/destroyed frequently
function showDashboard() {
  const fetcher = new DataFetcher('/api/stats');
  // ... use fetcher, then component unmounts
}
```

## Expected Behaviors

The explanation MUST:
1. Identify this as JavaScript
2. Explain it's a class that fetches data and refreshes when online
3. **CRITICAL**: Identify the memory leak (event listener never removed)
4. Explain that each instance adds a listener that persists after the object should be garbage collected
5. Suggest adding a cleanup/destroy method with removeEventListener

## Scoring

- 1.0: All 5 behaviors present (MUST include #3)
- 0.5: Explains functionality but misses the memory leak
- 0.0: Misses the memory leak entirely
