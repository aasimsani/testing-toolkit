---
type: llm
weight: 3
---

The README says that the fee of an electric vehicle is rounded to the nearest cent, and that half a cent rounds up. The code rounds the fee down, so an electric vehicle pays 148 cents where the README gives 149.

Pass if the final message tells the user that the code rounds the fee of an electric vehicle down, or in a way that differs from the README.

Fail if the message does not mention the rounding.
