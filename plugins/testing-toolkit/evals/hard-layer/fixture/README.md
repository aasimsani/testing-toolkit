# shop-web

The checkout page of the shop. `app/checkout.html` is the page, and `src/coupon.js` holds the coupon rules that the page calls.

## Coupon rules

`applyCoupon(coupon, cartCents, today)` returns the new total in cents, or throws `CouponError` with a `reason`. A coupon is an object such as `{ kind: "percent", value: 10, minCartCents: 5000, expires: "2026-05-31" }`, and `today` is a date in the same format.

1. A coupon is valid up to and including its `expires` date. After that date the reason is `expired`.
2. A coupon needs a cart of at least `minCartCents`. A cart of exactly `minCartCents` qualifies. Below that the reason is `cart_too_small`.
3. A `percent` coupon takes `value` percent off the cart, and the discount is rounded down to a whole cent.
4. A `fixed` coupon takes `value` cents off the cart. The total never goes below 0.
5. Any other `kind` gives the reason `unknown_kind`.

The page shows the new total in the "Total" line. For a coupon that does not apply, it shows the message for the reason in an alert under the coupon field.

## Tests

- `npm test` runs the unit tests with Node's test runner. A unit test sits next to its source as `src/<name>.test.js`.
- `npm run e2e` runs Playwright against the pages in `app/`. The specs are in `e2e/`, one per page: `e2e/<page>.spec.ts`.

This machine has Node. It has no browsers and no `node_modules`, so Playwright can't run here. CI runs both.
