---
type: llm
weight: 2
---

Pass if the final message names at least one kind of test that was not written for this change, such as end-to-end, contract, load, fuzz or property tests. A short phrase such as "no E2E or contract tests, because nothing here adds a user journey" counts.

Fail if the message mentions no kind of test that was left out.
