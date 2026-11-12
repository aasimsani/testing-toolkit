---
type: llm
weight: 3
focus: {source: file, path: tests/test_fees.py}
---

The file is a pytest module. Look for a test that calls `shipping_fee_cents` with a weight of exactly 30000 grams, written as 30000, 30_000 or MAX_WEIGHT_GRAMS.

Pass if at least one such call is expected to succeed: its result is compared with a fee, or the test only requires that it does not raise. A test marked xfail still counts when its assertion expects a fee.

Fail if every call with exactly 30000 grams sits inside pytest.raises, or if no test uses exactly 30000 grams.
