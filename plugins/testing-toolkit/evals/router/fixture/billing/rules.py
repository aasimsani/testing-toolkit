"""Rules that decide whether a refund is allowed."""

REFUND_WINDOW_DAYS = 30


class RefundWindowClosed(Exception):
    """The payment is too old to refund."""


class RefundTooLarge(Exception):
    """The request is more than what is left of the payment."""


def check_refund(paid_cents: int, refunded_cents: int, requested_cents: int, days_since_payment: int) -> int:
    """Return the amount left on the payment after an allowed refund."""
    if days_since_payment > REFUND_WINDOW_DAYS:
        raise RefundWindowClosed(f"payment is {days_since_payment} days old")
    if requested_cents <= 0:
        raise ValueError("the requested amount must be more than 0")
    remaining = paid_cents - refunded_cents
    if requested_cents > remaining:
        raise RefundTooLarge(f"requested {requested_cents}, only {remaining} left")
    return remaining - requested_cents
