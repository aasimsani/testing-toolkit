"""Reference result for the hard-property case. Each property is one README rule."""

import pytest
from hypothesis import example, given
from hypothesis import strategies as st

from busy.periods import merge_periods

# A period is built as a start and a length, so start <= end holds by construction.
# The small range makes overlapping and nested periods common.
period = st.tuples(st.integers(0, 60), st.integers(0, 20)).map(lambda p: (p[0], p[0] + p[1]))
periods = st.lists(period, max_size=8)


def minutes(some_periods):
    return {minute for start, end in some_periods for minute in range(start, end + 1)}


@pytest.mark.xfail(strict=True, reason="README rule 4. merge_periods([(1, 10), (2, 3)]) returns [(1, 3)].")
@given(periods)
@example([(1, 10), (2, 3)])
def test_result_covers_exactly_the_minutes_of_the_input(some_periods):
    assert minutes(merge_periods(list(some_periods))) == minutes(some_periods)


@given(periods)
@example([(1, 5), (5, 9)])
@example([(3, 4), (1, 2)])
def test_result_is_in_order_and_its_periods_share_no_minute(some_periods):
    result = merge_periods(list(some_periods))
    assert all(end < next_start for (_, end), (next_start, _) in zip(result, result[1:]))


@pytest.mark.xfail(strict=True, reason="README rule 5. merge_periods sorts the list that it receives.")
@given(periods)
@example([(5, 6), (1, 2)])
def test_input_list_is_left_unchanged(some_periods):
    before = list(some_periods)
    merge_periods(some_periods)
    assert some_periods == before


@given(periods, st.integers(0, 60).flatmap(lambda end: st.tuples(st.integers(end + 1, 99), st.just(end))))
def test_period_that_starts_after_its_end_is_rejected(some_periods, backwards):
    with pytest.raises(ValueError):
        merge_periods([*some_periods, backwards])
