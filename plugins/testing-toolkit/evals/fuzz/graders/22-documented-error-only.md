---
type: regex
weight: 2
target: {source: file, path: fuzz/fuzz_parse_config.py}
match: contains
---

except\s+\(?\s*(\w+\.)?ConfigError
