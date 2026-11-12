---
type: llm
weight: 2
---

Pass if the final message gives a reason why the store is tested against a real Postgres database, and not against a mock or an in-memory substitute. A reason such as "the idempotency rule depends on the unique constraint and ON CONFLICT" counts.

Fail if the message gives no reason for that choice, or if the store is not tested against a real Postgres database.
