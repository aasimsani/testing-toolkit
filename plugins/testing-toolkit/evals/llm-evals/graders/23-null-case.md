---
type: llm
weight: 2
---

Pass if the final message says that the suite checks a missing field: an invoice with no due date must give `null`, and the model must not invent a value.

Fail if the message mentions no such check.
