---
type: llm
weight: 3
focus: {source: file, path: tests/test_payslip_characterization.py}
---

The function under test puts the current time and a random uuid in its output.

Pass if the tests make that output repeatable: they patch, freeze or inject the clock and the uuid, or they mask or strip those two values before they compare.

Fail if any test compares output that still holds the real current time or a random id.
