---
type: llm
weight: 3
---

Pass if the final message says that the coupon rules are checked in unit tests, that the Playwright spec covers only the journey on the page, and gives a reason for that split. A reason such as "the rules are pure logic, so a browser test of each rule would be slow and would add nothing" counts.

Fail if the message gives no reason for where the checks of the rules went, or if it says that the rules are checked in Playwright.
