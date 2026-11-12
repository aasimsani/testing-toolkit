---
type: regex
weight: 1
target: {source: file, path: tests/test_tariff.py}
match: not_contains
---

assert_called|MagicMock|mocker\.|unittest\.mock
