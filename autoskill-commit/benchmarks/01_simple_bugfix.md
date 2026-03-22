# Benchmark: Simple Bug Fix

## Input Diff

```diff
diff --git a/src/utils.js b/src/utils.js
index 1234567..abcdefg 100644
--- a/src/utils.js
+++ b/src/utils.js
@@ -10,7 +10,7 @@ function calculateTotal(items) {
   let total = 0;
   for (const item of items) {
-    total += item.price;
+    total += item.price || 0;
   }
   return total;
 }
```

## Expected Behaviors

The commit message MUST:
1. Use "fix" type (this fixes a bug)
2. Be in imperative mood
3. Mention null/undefined handling or NaN prevention
4. Be under 50 characters for subject
5. NOT include the diff itself in the message

## Scoring

- 1.0: All 5 behaviors present
- 0.5: Correct type and mood but vague description
- 0.0: Wrong type or past tense
