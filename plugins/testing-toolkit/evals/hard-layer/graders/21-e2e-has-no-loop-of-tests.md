---
type: regex
weight: 1
target: {source: file, path: e2e/checkout.spec.ts}
match: not_contains
flags: s
---

(\bfor\s*\(|\.forEach\s*\().*?\btest\s*\(
