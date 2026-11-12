"""Fee for one stay in the car park."""

FREE_MINUTES = 15
BLOCK_MINUTES = 30
BLOCK_CENTS = 175
MAX_FEE_CENTS = 2400
MAX_STAY_MINUTES = 1440
EV_PERCENT = 85


def parking_fee_cents(minutes: int, ev: bool = False) -> int:
    """Return the fee in cents for a stay of `minutes`."""
    if minutes < 0 or minutes > MAX_STAY_MINUTES:
        raise ValueError(f"stay out of range: {minutes}")
    if minutes < FREE_MINUTES:
        return 0
    blocks = -(-minutes // BLOCK_MINUTES)
    fee = blocks * BLOCK_CENTS
    if ev:
        fee = fee * EV_PERCENT // 100
    return min(fee, MAX_FEE_CENTS)
