---
type: llm
weight: 3
---

The README says that a booking of exactly `minBookingCents` qualifies for a coupon. The code rejects that booking with `booking_too_small`.

Pass if the final message tells the user about this disagreement between the code and the README.

Fail if the message does not mention it.
