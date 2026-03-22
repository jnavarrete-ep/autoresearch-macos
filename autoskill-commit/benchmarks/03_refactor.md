# Benchmark: Refactoring

## Input Diff

```diff
diff --git a/src/components/Button.jsx b/src/components/Button.jsx
index 1234567..abcdefg 100644
--- a/src/components/Button.jsx
+++ b/src/components/Button.jsx
@@ -1,25 +1,12 @@
-import React from 'react';
-
-class Button extends React.Component {
-  constructor(props) {
-    super(props);
-    this.handleClick = this.handleClick.bind(this);
-  }
-
-  handleClick() {
-    if (this.props.onClick) {
-      this.props.onClick();
-    }
-  }
-
-  render() {
-    return (
-      <button onClick={this.handleClick} className={this.props.className}>
-        {this.props.children}
-      </button>
-    );
-  }
-}
+function Button({ onClick, className, children }) {
+  return (
+    <button onClick={onClick} className={className}>
+      {children}
+    </button>
+  );
+}

 export default Button;
```

## Expected Behaviors

The commit message MUST:
1. Use "refactor" type (behavior unchanged, code improved)
2. Mention conversion from class to function component
3. NOT claim this is a fix or feature
4. Be in imperative mood
5. Subject under 50 characters

## Scoring

- 1.0: All behaviors present
- 0.5: Correct type but doesn't mention class→function
- 0.0: Uses "fix" or "feat" type
