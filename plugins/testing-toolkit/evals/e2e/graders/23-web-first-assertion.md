---
type: regex
weight: 2
target: {source: file, path: e2e/signup.spec.ts}
match: contains
---

await expect\(.*\)\.(not\.)?to(BeVisible|HaveURL|HaveText|ContainText|BeHidden)
