---
type: llm
weight: 3
focus: {source: file, path: src/coupon.test.js}
---

The file holds unit tests for `applyCoupon(coupon, bookingCents, today)`. Look for a test in which `bookingCents` equals the coupon's `minBookingCents` exactly.

Pass if at least one such test expects the coupon to apply, which means that it expects a new amount. A test marked todo or expected to fail still counts when its assertion expects an amount.

Fail if every such test expects `booking_too_small`, or if no test uses a booking that equals `minBookingCents`.
