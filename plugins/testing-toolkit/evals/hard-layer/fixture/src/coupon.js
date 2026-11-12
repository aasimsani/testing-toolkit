export class CouponError extends Error {
  constructor(reason) {
    super(reason);
    this.reason = reason;
  }
}

// Dates are ISO strings such as "2026-05-31", which compare in date order.
export function applyCoupon(coupon, bookingCents, today) {
  if (today > coupon.expires) throw new CouponError("expired");
  if (bookingCents <= coupon.minBookingCents) throw new CouponError("booking_too_small");
  if (coupon.kind === "percent") {
    return bookingCents - Math.floor((bookingCents * coupon.value) / 100);
  }
  if (coupon.kind === "fixed") {
    return Math.max(0, bookingCents - coupon.value);
  }
  throw new CouponError("unknown_kind");
}
