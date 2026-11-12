---
type: regex
weight: 1
target: {source: file, path: evals/promptfooconfig.yaml}
match: contains
flags: i
---

v[0-9]+|version
