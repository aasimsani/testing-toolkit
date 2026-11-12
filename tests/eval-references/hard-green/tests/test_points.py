from datetime import date

from loyalty.points import summary, tier, valid_points

TODAY = date(2026, 3, 1)


def test_points_earned_today_count():
    assert valid_points([(TODAY, 40)], TODAY) == 40


def test_points_earned_365_days_ago_still_count():
    assert valid_points([(date(2025, 3, 1), 40)], TODAY) == 40


def test_points_earned_366_days_ago_have_expired():
    assert valid_points([(date(2025, 2, 28), 40)], TODAY) == 0


def test_tier_starts_at_its_threshold():
    assert tier(249) == "basic"
    assert tier(250) == "silver"
    assert tier(1000) == "gold"


def test_summary_line():
    assert summary("Ada", [(date(2026, 1, 10), 1200)], TODAY) == "Ada: gold, 1200 points"
