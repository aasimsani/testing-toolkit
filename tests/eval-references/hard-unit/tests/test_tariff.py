"""Reference result for the hard-unit case. Every expected value comes from the README."""

import pytest

from parking.tariff import parking_fee_cents


@pytest.mark.parametrize(
    ("minutes", "fee"),
    [(0, 0), (16, 175), (30, 175), (31, 350), (390, 2275), (391, 2400), (480, 2400), (1440, 2400)],
)
def test_fee_by_length_of_stay(minutes, fee):
    assert parking_fee_cents(minutes) == fee


@pytest.mark.xfail(strict=True, reason="README rule 1 makes 15 minutes free. The code charges 175.")
def test_stay_of_exactly_15_minutes_is_free():
    assert parking_fee_cents(15) == 0


def test_electric_vehicle_pays_85_percent():
    assert parking_fee_cents(120, ev=True) == 595


@pytest.mark.xfail(strict=True, reason="README rule 4 rounds 148.75 to 149. The code rounds down to 148.")
def test_electric_vehicle_fee_rounds_to_the_nearest_cent():
    assert parking_fee_cents(30, ev=True) == 149


@pytest.mark.xfail(strict=True, reason="README rule 4 rounds 297.5 up to 298. The code rounds down to 297.")
def test_electric_vehicle_fee_rounds_half_a_cent_up():
    assert parking_fee_cents(60, ev=True) == 298


@pytest.mark.xfail(strict=True, reason="README rule 4 applies the discount after the limit: 2040. The code gives 2380.")
def test_electric_vehicle_discount_applies_after_the_limit():
    assert parking_fee_cents(480, ev=True) == 2040


@pytest.mark.parametrize("minutes", [-1, 1441])
def test_stay_out_of_range_is_rejected(minutes):
    with pytest.raises(ValueError):
        parking_fee_cents(minutes)
