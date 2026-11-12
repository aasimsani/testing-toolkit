---
type: llm
weight: 2
focus: {source: file, path: src/coupon.test.js}
---

The file holds unit tests for `applyCoupon(coupon, cartCents, today)`.

Pass if at least one test calls it with `today` equal to the coupon's `expires` date and expects the coupon to apply.

Fail if no test uses the `expires` date itself as `today`.
