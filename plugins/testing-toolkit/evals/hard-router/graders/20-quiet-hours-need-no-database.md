---
type: regex
weight: 1
target: {source: file, path: tests/test_quiet_hours.py}
match: not_contains
flags: i
---

psycopg|testcontainers|PostgresContainer|sqlite
