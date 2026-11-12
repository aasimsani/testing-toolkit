---
type: llm
weight: 1
---

Pass if the final message says what to do with a crash that the fuzzer finds: keep the crashing input as a regression input, in the corpus or in a test.

Fail if the message says nothing about crashing inputs.
