---
type: llm
weight: 2
focus: {source: file, path: tests/test_periods_properties.py}
---

Pass if at least one test checks that `merge_periods` leaves the list that it receives unchanged, for example by comparing the list after the call with a copy made before the call.

Fail if no test checks that.
