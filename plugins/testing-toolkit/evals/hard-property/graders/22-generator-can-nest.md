---
type: llm
weight: 3
focus: {source: file, path: tests/test_periods_properties.py}
---

The file holds Hypothesis tests for `merge_periods`. Look at the strategy that generates the list of periods.

Pass if the strategy can generate periods that overlap, including one period that lies inside another.

Fail if the strategy generates only periods that share no minute, or if a filter or `assume` removes the overlapping ones.
