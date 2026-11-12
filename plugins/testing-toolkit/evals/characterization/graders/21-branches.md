---
type: llm
weight: 2
focus: {source: file, path: tests/test_payslip_characterization.py}
---

Pass if the tests include an input with more than 160 hours, which reaches the overtime branch, and an input for a union member, which reaches the dues branch.

Fail if either input is missing.
