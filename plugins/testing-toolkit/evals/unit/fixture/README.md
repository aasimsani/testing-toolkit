# parcel

`parcel/fees.py` computes the shipping fee for one parcel, in cents.

## Rules

`shipping_fee_cents(weight_grams, express=False)` returns the fee.

1. A parcel of up to 2000 g costs 499 cents.
2. A heavier parcel costs 499 cents plus 150 cents for each started 1000 g above 2000 g. A parcel of 2001 g costs 649 cents, and so does a parcel of 3000 g.
3. Express delivery adds 50% to the fee, rounded down to a whole cent.
4. The weight must be more than 0 g and at most 30000 g. Any other weight raises `ValueError`.

## Running tests

```bash
.venv/bin/python -m pytest -q
```
