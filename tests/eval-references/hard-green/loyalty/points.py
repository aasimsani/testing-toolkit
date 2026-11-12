"""Points of a member of the loyalty scheme."""

from datetime import date

MAX_AGE_DAYS = 365
GOLD_FROM = 1000
SILVER_FROM = 250


def valid_points(entries: list[tuple[date, int]], today: date) -> int:
    """Return the sum of the points that have not expired."""
    total = 0
    for earned_on, points in entries:
        if (today - earned_on).days > MAX_AGE_DAYS:
            continue
        total += points
    return total


def tier(points: int) -> str:
    """Return the name of the tier for a number of valid points."""
    if points >= GOLD_FROM:
        return "gold"
    if points >= SILVER_FROM:
        return "silver"
    return "basic"


def summary(name: str, entries: list[tuple[date, int]], today: date) -> str:
    """Return the line that the account page shows for a member."""
    points = valid_points(entries, today)
    return f"{name}: {tier(points)}, {points} points"
