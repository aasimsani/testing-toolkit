---
type: regex
weight: 2
target: {source: file, path: evals/promptfooconfig.yaml}
match: contains
flags: m
---

temperature\s*:\s*0(\.0)?\s*(\}|,|#|$)
