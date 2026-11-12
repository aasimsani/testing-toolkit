---
type: llm
weight: 3
focus: {source: file, path: src/coupon.test.js}
---

The file holds unit tests for `applyCoupon(coupon, cartCents, today)`. Look for a test in which `cartCents` equals the coupon's `minCartCents` exactly.

Pass if at least one such test expects the coupon to apply, which means that it expects a new total. A test marked todo or expected to fail still counts when its assertion expects a total.

Fail if every such test expects `cart_too_small`, or if no test uses a cart that equals `minCartCents`.
