# billing

Refunds for the shop. Production runs Postgres 16.2, as `docker-compose.yml` shows. The schema is in `migrations/001_refunds.sql`.

## The change

Two new modules:

- `billing/rules.py` decides whether a refund is allowed.
- `billing/store.py` records refunds in Postgres.

The support dashboard is a separate repo. It calls this code through the existing `/refunds` handler, which this change does not touch.

## Rules

`check_refund(paid_cents, refunded_cents, requested_cents, days_since_payment)`:

1. A refund is allowed for 30 days after the payment, day 30 included. After that it raises `RefundWindowClosed`.
2. The requested amount must be more than 0. Anything else raises `ValueError`.
3. The requested amount may be at most what is left of the payment: `paid_cents - refunded_cents`. More than that raises `RefundTooLarge`.
4. When the refund is allowed, the function returns the amount left after it.

`RefundStore(conn)`:

5. `record(payment_id, amount_cents, idempotency_key)` stores one refund and returns `True`. A second call with the same idempotency key stores nothing and returns `False`.
6. `total_refunded(payment_id)` returns the sum of the refunds for a payment, or 0 when there are none.
7. The database rejects a refund whose amount is 0 or less.

## Conventions

Tests live in `tests/`, one file per module: `tests/test_<module>.py`. Each test file holds its own fixtures, and the repo has no `conftest.py`.
