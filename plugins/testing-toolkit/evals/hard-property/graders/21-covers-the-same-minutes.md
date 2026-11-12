---
type: llm
weight: 3
focus: {source: file, path: tests/test_periods_properties.py}
---

The file holds Hypothesis tests for `merge_periods`.

Pass if at least one property compares the minutes that the result covers with the minutes that the input covers, or compares the result with a simple reference implementation that the test file defines.

Fail if the properties check only the order of the result, that its periods share no minute, its length, or that a second call changes nothing.
