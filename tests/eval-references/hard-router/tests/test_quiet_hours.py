"""Reference result for the hard-router case: unit tests, because the bugs are in the logic."""

from datetime import datetime, timezone

import pytest

from notify.quiet_hours import is_quiet


def utc(hour, minute=0):
    return datetime(2026, 1, 15, hour, minute, tzinfo=timezone.utc)


SEVEN_IS_NOT_QUIET = pytest.mark.xfail(
    strict=True, reason="README rule 1 says 07:00 itself is not quiet. The code says it is."
)


# Asia/Karachi is 5 hours ahead of UTC all year, so 17:00 UTC is 22:00 local time.
@pytest.mark.parametrize(
    ("now_utc", "quiet"),
    [
        (utc(16, 59), False),
        (utc(17, 0), True),
        (utc(1, 59), True),
        pytest.param(utc(2, 0), False, marks=SEVEN_IS_NOT_QUIET),
        (utc(2, 1), False),
    ],
)
def test_quiet_hours_follow_the_recipients_zone(now_utc, quiet):
    assert is_quiet(now_utc, "Asia/Karachi") is quiet
