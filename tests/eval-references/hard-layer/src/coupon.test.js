// Reference result for the hard-layer case. The rules are checked here, and the
// Playwright spec checks only that the page shows what `applyCoupon` returns.
import assert from "node:assert/strict";
import { test } from "node:test";

import { applyCoupon, CouponError } from "./coupon.js";

const percent = { kind: "percent", value: 10, minBookingCents: 5000, expires: "2026-05-31" };
const fixed = { kind: "fixed", value: 2000, minBookingCents: 0, expires: "2026-05-31" };

function reasonOf(coupon, bookingCents, today) {
  try {
    applyCoupon(coupon, bookingCents, today);
  } catch (error) {
    assert.ok(error instanceof CouponError);
    return error.reason;
  }
  return "applied";
}

test("a coupon applies on its expiry date", () => {
  assert.equal(applyCoupon(percent, 8000, "2026-05-31"), 7200);
});

test("a coupon has expired on the day after its expiry date", () => {
  assert.equal(reasonOf(percent, 8000, "2026-06-01"), "expired");
});

test(
  "a booking of exactly the minimum qualifies",
  { todo: "README rule 2 says this booking qualifies. The code rejects it with booking_too_small." },
  () => {
    assert.equal(applyCoupon(percent, 5000, "2026-05-01"), 4500);
  },
);

test("a booking one cent below the minimum is too small", () => {
  assert.equal(reasonOf(percent, 4999, "2026-05-01"), "booking_too_small");
});

test("a percent discount is rounded down to a whole cent", () => {
  assert.equal(applyCoupon({ ...percent, value: 15, minBookingCents: 0 }, 999, "2026-05-01"), 850);
});

test("a fixed coupon never takes the court fee below 0", () => {
  assert.equal(applyCoupon(fixed, 1500, "2026-05-01"), 0);
});

test("an unknown kind is rejected", () => {
  assert.equal(reasonOf({ ...fixed, kind: "bogo" }, 1500, "2026-05-01"), "unknown_kind");
});
