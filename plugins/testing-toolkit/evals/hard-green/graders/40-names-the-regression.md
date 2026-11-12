---
type: llm
weight: 3
---

One of the failing tests checks that points earned exactly 365 days ago still count. The README has the same rule, so that test is correct, and the code is wrong: it drops points that are exactly 365 days old.

Pass if the final message tells the user that this failure comes from a bug in the code, or that this test is not out of date.

Fail if the message treats that test as out of date, or does not mention it.
