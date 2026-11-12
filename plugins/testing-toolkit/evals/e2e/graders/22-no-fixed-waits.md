---
type: regex
weight: 3
target: {source: file, path: e2e/signup.spec.ts}
match: not_contains
---

waitForTimeout|setTimeout|describe\.serial
