# Benchmark: Multi-file Change

## Input Diff

```diff
diff --git a/src/models/User.js b/src/models/User.js
index 1234567..abcdefg 100644
--- a/src/models/User.js
+++ b/src/models/User.js
@@ -8,6 +8,7 @@ const userSchema = new Schema({
   email: { type: String, required: true, unique: true },
   password: { type: String, required: true },
   createdAt: { type: Date, default: Date.now },
+  lastLoginAt: { type: Date },
 });

diff --git a/src/api/auth.js b/src/api/auth.js
index 1234567..abcdefg 100644
--- a/src/api/auth.js
+++ b/src/api/auth.js
@@ -12,6 +12,9 @@ export async function login(email, password) {
     throw new AuthError('Invalid credentials');
   }

+  // Track last login time
+  await User.updateOne({ _id: user._id }, { lastLoginAt: new Date() });
+
   const token = generateToken(user);
   return { user, token };
 }
diff --git a/src/api/users.js b/src/api/users.js
index 1234567..abcdefg 100644
--- a/src/api/users.js
+++ b/src/api/users.js
@@ -15,6 +15,7 @@ export async function getUser(id) {
     id: user._id,
     email: user.email,
     createdAt: user.createdAt,
+    lastLoginAt: user.lastLoginAt,
   };
 }
```

## Expected Behaviors

The commit message MUST:
1. Use "feat" type (adds new functionality)
2. Summarize the overall change (last login tracking)
3. NOT list each file separately in subject
4. Be cohesive (one feature, not three changes)
5. Subject under 50 characters

## Scoring

- 1.0: Cohesive message about the feature
- 0.5: Mentions feature but lists files
- 0.0: Treats as unrelated changes or uses wrong type
