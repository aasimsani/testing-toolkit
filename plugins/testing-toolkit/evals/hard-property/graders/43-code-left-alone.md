---
type: regex
weight: 2
target: {source: file, path: busy/periods.py}
match: contains
flags: s
---

periods\.sort\(\).*merged\[-1\] = \(last_start, end\)
