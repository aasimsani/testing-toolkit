export class CouponError extends Error {
  constructor(reason) {
    super(reason);
    this.reason = reason;
  }
}

// Dates are ISO strings such as "2026-05-31", which compare in date order.
export function applyCoupon(coupon, cartCents, today) {
  if (today > coupon.expires) throw new CouponError("expired");
  if (cartCents <= coupon.minCartCents) throw new CouponError("cart_too_small");
  if (coupon.kind === "percent") {
    return cartCents - Math.floor((cartCents * coupon.value) / 100);
  }
  if (coupon.kind === "fixed") {
    return Math.max(0, cartCents - coupon.value);
  }
  throw new CouponError("unknown_kind");
}
