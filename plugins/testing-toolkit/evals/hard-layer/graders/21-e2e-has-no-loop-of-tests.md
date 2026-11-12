---
type: regex
weight: 1
target: {source: file, path: e2e/booking.spec.ts}
match: not_contains
flags: s
---

(\bfor\s*\(|\.forEach\s*\().*?\btest\s*\(
