---
type: regex
weight: 3
target: {source: file, path: e2e/signup.spec.ts}
match: not_contains
---

(locator|click|fill|check|\$\$?)\(\s*['"`]\s*(\.[A-Za-z]|#[A-Za-z]|//|xpath=|css=)
