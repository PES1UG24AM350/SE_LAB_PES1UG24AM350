import pytest

from mobile_data_plan import (
    overage_charge,
    recharge_allowed,
    validity_status,
)


# Overage charge tests
def test_basic_plan_no_overage():
    assert overage_charge("basic", 2, False, False) == 0


def test_standard_plan_overage():
    assert overage_charge("standard", 7, False, False) == 30


def test_premium_plan_roaming():
    assert overage_charge("premium", 12, True, False) == 80


def test_loyal_customer_extra_allowance():
    assert overage_charge("basic", 3, False, True) == 0


def test_large_roaming_overage():
    assert overage_charge("basic", 15, True, False) == 715


def test_large_non_roaming_overage():
    assert overage_charge("basic", 15, False, False) == 325


def test_exactly_ten_extra_gb():
    assert overage_charge("basic", 12, False, False) == 150


def test_unknown_plan():
    with pytest.raises(ValueError, match="unknown plan"):
        overage_charge("gold", 5, False, False)


def test_negative_usage():
    with pytest.raises(ValueError, match="invalid data usage"):
        overage_charge("basic", -1, False, False)


# Recharge tests
def test_kyc_pending_allowed():
    assert recharge_allowed(200, 5, True) is True


def test_kyc_pending_denied():
    assert recharge_allowed(201, 0, True) is False


def test_recharge_over_limit():
    assert recharge_allowed(2001, 0, False) is False


def test_two_pending_recharges():
    assert recharge_allowed(500, 2, False) is True


def test_three_pending_recharges():
    assert recharge_allowed(500, 3, False) is False


# Validity tests
def test_prepaid_active():
    assert validity_status(5, True, False) == "active"


def test_postpaid_active():
    assert validity_status(5, False, False) == "active"


def test_addon_active():
    assert validity_status(3, True, True) == "active"


def test_grace_period():
    assert validity_status(-5, True, False) == "grace"


def test_expired():
    assert validity_status(-16, True, False) == "expired"
