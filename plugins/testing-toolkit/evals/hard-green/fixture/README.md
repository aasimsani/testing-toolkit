# loyalty

`loyalty/points.py` keeps the points of a member of the loyalty scheme.

## Rules

1. `valid_points(entries, today)` returns the sum of the points that have not expired. An entry is a pair `(earned_on, points)`.
2. Points expire when they are more than 365 days old. Points that a member earned exactly 365 days before `today` still count.
3. `tier(points)` returns `"gold"` from 1000 points, `"silver"` from 250 points, and `"basic"` below that.
4. `summary(name, entries, today)` returns the line that the account page shows, such as `Ada: gold, 1200 points`.

## Running tests

```bash
.venv/bin/python -m pytest -q
```
