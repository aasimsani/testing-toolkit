---
type: llm
weight: 3
---

The code gives a wrong result when one period lies inside another. `merge_periods([(1, 10), (2, 3)])` returns `[(1, 3)]`, which loses the minutes 4 to 10.

Pass if the final message reports this bug and gives an input that shows it.

Fail if the message does not mention it, or says that every property holds.
