---
type: llm
weight: 2
---

Pass if the final message gives a reason why the outbox is tested against a real Postgres database, and not against a mock or an in-memory substitute. A reason such as "SKIP LOCKED and the unique constraint only behave this way in Postgres" counts.

Fail if the message gives no reason for that choice, or if the outbox is not tested against a real Postgres database.
