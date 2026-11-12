"""Merge the busy periods of a calendar."""


def merge_periods(periods: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Return `periods` with every two periods that share a minute merged."""
    for start, end in periods:
        if start > end:
            raise ValueError(f"start after end: {(start, end)}")
    if not periods:
        return []
    periods.sort()
    merged = [periods[0]]
    for start, end in periods[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, end)
        else:
            merged.append((start, end))
    return merged
