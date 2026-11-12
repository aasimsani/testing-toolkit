"""Quiet hours, during which a recipient gets no message."""

from datetime import datetime, time
from zoneinfo import ZoneInfo

QUIET_FROM = time(22, 0)
QUIET_UNTIL = time(7, 0)


def is_quiet(now_utc: datetime, tz_name: str) -> bool:
    """Return whether `now_utc` falls in the quiet hours of the time zone `tz_name`."""
    local = now_utc.astimezone(ZoneInfo(tz_name)).time()
    return local >= QUIET_FROM or local <= QUIET_UNTIL
