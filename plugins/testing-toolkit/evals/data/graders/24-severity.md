---
type: regex
weight: 2
target: {source: file, path: models/schema.yml}
match: contains
---

severity\s*:\s*['"]?warn
