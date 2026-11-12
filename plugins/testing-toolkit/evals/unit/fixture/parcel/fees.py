"""Shipping fees in cents."""

BASE_FEE_CENTS = 499
BASE_WEIGHT_GRAMS = 2000
STEP_GRAMS = 1000
STEP_FEE_CENTS = 150
MAX_WEIGHT_GRAMS = 30000


def shipping_fee_cents(weight_grams: int, express: bool = False) -> int:
    """Return the fee for one parcel, in cents."""
    if weight_grams <= 0 or weight_grams >= MAX_WEIGHT_GRAMS:
        raise ValueError("weight must be between 1 and 30000 grams")
    fee = BASE_FEE_CENTS
    if weight_grams > BASE_WEIGHT_GRAMS:
        extra = weight_grams - BASE_WEIGHT_GRAMS
        steps = -(-extra // STEP_GRAMS)
        fee += steps * STEP_FEE_CENTS
    if express:
        fee = fee * 3 // 2
    return fee
