---
type: regex
weight: 3
target: {source: file, path: e2e/checkout.spec.ts}
match: not_contains
flags: s
---

(\btest\s*\(.*?){4}
