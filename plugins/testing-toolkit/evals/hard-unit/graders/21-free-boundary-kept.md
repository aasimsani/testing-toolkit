---
type: llm
weight: 3
focus: {source: file, path: tests/test_tariff.py}
---

The file is a pytest module. Look for a test that calls `parking_fee_cents` with a stay of exactly 15 minutes, written as 15 or FREE_MINUTES.

Pass if at least one such call expects a fee of 0. A test marked xfail still counts when its assertion expects 0.

Fail if every call with exactly 15 minutes expects 175 or another fee above 0, or if no test uses exactly 15 minutes.
