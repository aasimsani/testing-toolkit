---
type: llm
weight: 2
---

Pass if the final message says that the suite has a case for an invoice that leaves a field out, such as the due date or the invoice number, where the expected value is null.

Fail if the message mentions no case with a missing field.
