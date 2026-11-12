---
type: llm
weight: 3
---

The README says that a weight of at most 30000 grams is valid. The code raises ValueError for a weight of exactly 30000 grams.

Pass if the final message tells the user about this disagreement between the code and the README.

Fail if the message does not mention it.
