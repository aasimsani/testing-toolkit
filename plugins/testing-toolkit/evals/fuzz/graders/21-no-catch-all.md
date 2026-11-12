---
type: regex
weight: 3
target: {source: file, path: fuzz/fuzz_parse_config.py}
match: not_contains
---

except\s*:|except\s+\(?\s*(Exception|BaseException)\b
