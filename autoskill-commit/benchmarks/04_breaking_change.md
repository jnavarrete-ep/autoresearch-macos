# Benchmark: Breaking Change

## Input Diff

```diff
diff --git a/src/api/auth.js b/src/api/auth.js
index 1234567..abcdefg 100644
--- a/src/api/auth.js
+++ b/src/api/auth.js
@@ -5,12 +5,14 @@
  * @param {string} password
- * @returns {Object} User object with token
+ * @returns {Object} Auth response with accessToken and refreshToken
  */
-export async function login(email, password) {
+export async function login(email, password, options = {}) {
   const user = await validateCredentials(email, password);
-  const token = generateToken(user);
-  return { user, token };
+  const accessToken = generateAccessToken(user);
+  const refreshToken = generateRefreshToken(user);
+  return {
+    accessToken,
+    refreshToken,
+    expiresIn: options.expiresIn || 3600
+  };
 }
```

## Expected Behaviors

The commit message MUST:
1. Use "feat" type with BREAKING CHANGE note (API changed)
2. Mention the token structure change
3. Include "BREAKING" or "!" indicator
4. Explain migration in body
5. Subject under 50 characters

## Scoring

- 1.0: Correctly identifies breaking change with proper notation
- 0.5: Good message but misses breaking change indicator
- 0.0: Treats as non-breaking change
