---
type: regex
weight: 3
target: {source: file, path: tests/test_outbox.py}
match: not_contains
flags: i
---

sqlite|:memory:|MagicMock|unittest\.mock|mocker\.|create_autospec
