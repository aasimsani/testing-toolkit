# parking

`parking/tariff.py` computes the fee for one stay in the car park, in cents.

## Rules

`parking_fee_cents(minutes, ev=False)` returns the fee.

1. A stay of up to 15 minutes is free.
2. A longer stay costs 175 cents for each started 30 minutes, counted from the start of the stay. A stay of 16 minutes costs 175 cents, and so does a stay of 30 minutes.
3. The fee for one stay is at most 2400 cents. A stay of 8 hours costs 2400 cents.
4. An electric vehicle pays 85% of the fee. The discount applies after the limit of rule 3. The result is rounded to the nearest cent, and half a cent rounds up. An electric vehicle that parks for 2 hours pays 595 cents.
5. The stay must be at least 0 minutes and at most 1440 minutes. Any other value raises `ValueError`.

## Running tests

```bash
.venv/bin/python -m pytest -q
```
