---
type: llm
weight: 2
focus: {source: file, path: tests/test_quiet_hours.py}
---

The file holds tests for `is_quiet(now_utc, tz_name)`. Quiet hours run from 22:00 to 07:00 local time.

Pass if the tests check both ends of the quiet hours: one test uses a moment that is exactly 22:00 local time, and one uses a moment that is exactly 07:00 local time.

Fail if either of the two moments is missing.
