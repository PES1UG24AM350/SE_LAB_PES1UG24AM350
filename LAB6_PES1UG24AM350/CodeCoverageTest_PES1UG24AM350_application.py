import pytest

from mobile_data_plan import (
    overage_charge,
    recharge_allowed,
    validity_status,
)


# Test overage charge calculations
def test_basic_plan_no_extra_data():
    assert overage_charge("basic", 2, False, False) == 0


def test_standard_plan_overage():
    assert overage_charge("standard", 7, False, False) == 30


def test_premium_plan_roaming():
    assert overage_charge("premium", 12, True, False) == 80


def test_loyal_customer_extra_data_allowance():
    assert overage_charge("basic", 3, False, True) == 0


def test_large_roaming_overage():
    assert overage_charge("basic", 15, True, False) == 715


def test_unknown_plan():
    with pytest.raises(ValueError, match="unknown plan"):
        overage_charge("gold", 5, False, False)


def test_negative_data_usage():
    with pytest.raises(ValueError, match="invalid data usage"):
        overage_charge("basic", -1, False, False)


# Test recharge eligibility
def test_kyc_pending_recharge_allowed():
    assert recharge_allowed(200, 5, True) is True


def test_kyc_pending_recharge_exceeds_limit():
    assert recharge_allowed(201, 0, True) is False


def test_recharge_amount_exceeds_limit():
    assert recharge_allowed(2001, 0, False) is False


def test_recharge_allowed_with_two_pending():
    assert recharge_allowed(500, 2, False) is True


def test_recharge_denied_with_too_many_pending():
    assert recharge_allowed(500, 3, False) is False


# Test plan validity
def test_prepaid_active():
    assert validity_status(5, True, False) == "active"


def test_postpaid_active():
    assert validity_status(5, False, False) == "active"


def test_active_with_addon():
    assert validity_status(3, True, True) == "active"


def test_grace_period():
    assert validity_status(-5, True, False) == "grace"


def test_expired_plan():
    assert validity_status(-16, True, False) == "expired"
