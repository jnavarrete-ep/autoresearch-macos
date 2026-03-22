# Benchmark: New Feature

## Input Diff

```diff
diff --git a/src/api/users.js b/src/api/users.js
index 1234567..abcdefg 100644
--- a/src/api/users.js
+++ b/src/api/users.js
@@ -45,6 +45,24 @@ export async function getUser(id) {
   return user;
 }

+export async function deleteUser(id) {
+  const user = await db.users.findById(id);
+  if (!user) {
+    throw new NotFoundError('User not found');
+  }
+
+  // Soft delete - mark as deleted instead of removing
+  await db.users.update(id, {
+    deletedAt: new Date(),
+    status: 'deleted'
+  });
+
+  // Revoke all active sessions
+  await db.sessions.deleteMany({ userId: id });
+
+  return { success: true };
+}
```

## Expected Behaviors

The commit message MUST:
1. Use "feat" type (this adds new functionality)
2. Mention "delete" or "remove" user functionality
3. Be in imperative mood ("Add" not "Added")
4. Optionally mention soft delete in body
5. Subject under 50 characters

## Scoring

- 1.0: All behaviors present
- 0.5: Correct but mentions implementation details in subject
- 0.0: Wrong type or describes it as a fix
