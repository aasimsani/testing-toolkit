---
type: llm
weight: 2
---

Pass if the final message pairs at least one test, case or check that it wrote with a specific bug or break that would make that test fail. The usual form is a table row or a list item that names the test and names the bug. A sentence such as "this test fails if X" also counts.

Whether the tests were run does not matter.

Fail if the message names no bug next to a test. A bug that the message reports but that no test checks does not count. A warning that a test might fail for a reason that is not a bug does not count.
