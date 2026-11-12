---
type: llm
weight: 3
---

The code gives a wrong result when one period lies inside another. The merged period ends too early, so the result loses minutes of the outer period.

Pass if the final message reports this bug and gives an input that shows it. Any input counts.

Fail if the message does not mention this bug, or says that every property holds.
