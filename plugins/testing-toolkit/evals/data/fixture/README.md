# analytics (dbt)

A dbt project on dbt 1.9. `models/staging/stg_orders.sql` cleans the raw orders, and `models/marts/dim_customers.sql` builds one row per customer.

## `dim_customers`

One row per `customer_id`.

- `first_order_date` is the date of the customer's earliest order that was not cancelled.
- `lifetime_orders` counts the customer's orders that were not cancelled.
- `lifetime_value_cents` sums `amount_cents` over those orders.
- A customer whose orders were all cancelled still gets a row, with `lifetime_orders = 0`, `lifetime_value_cents = 0` and a null `first_order_date`.

## Source

The ingestion job loads `shop.orders` every hour. Its columns are `order_id` (the primary key), `customer_id`, `status` (`placed`, `shipped` or `cancelled`), `amount_cents`, `ordered_at`, and `coupon_code`, which is empty for most orders. `_loaded_at` is the load time.

No tests exist yet.
