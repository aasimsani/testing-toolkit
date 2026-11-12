# busy

`busy/periods.py` merges the busy periods of a calendar.

## Rules

`merge_periods(periods)` takes a list of periods and returns the merged list. A period is a pair of whole minutes `(start, end)`, and both ends belong to the period.

1. Two periods that share at least one minute become one period. `(1, 5)` and `(5, 9)` become `(1, 9)`.
2. Periods that share no minute stay apart. `(1, 2)` and `(3, 4)` stay as they are.
3. The result is in order of start, and no two periods in it share a minute.
4. The result covers exactly the minutes that the input covers.
5. The input may be in any order, and `merge_periods` does not change the list that it receives.
6. A period whose start is after its end raises `ValueError`.

## Running tests

```bash
.venv/bin/python -m pytest -q
```
