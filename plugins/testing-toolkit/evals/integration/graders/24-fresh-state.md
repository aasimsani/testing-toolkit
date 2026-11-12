---
type: regex
weight: 2
target: {source: file, path: tests/test_repo.py}
match: contains
flags: i
---

rollback|truncate|drop table|delete from
