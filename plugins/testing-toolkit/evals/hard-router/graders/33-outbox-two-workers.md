---
type: llm
weight: 3
focus: {source: file, path: tests/test_outbox.py}
---

The file holds tests for an outbox table in Postgres. The rule under test is that two workers that call `claim` at the same time never get the same message.

Pass if at least one test uses two separate database connections, or two transactions that are open at the same time, and checks that the two claims share no message.

Fail if every test calls `claim` on a single connection, or calls it a second time only after the first claim has committed.
