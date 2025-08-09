import random
import pytest
from source.referral_bonus import ReferralBonus


@pytest.fixture
def small_network():
    sim = ReferralBonus()
    # Build a small referral graph
    sim.give_referral("A", "B")
    sim.give_referral("A", "C")
    sim.give_referral("B", "D")
    sim.give_referral("C", "E")
    sim.give_referral("E", "F")
    sim.give_referral("D", "G")
    return sim


@pytest.fixture
def large_network():
    sim = ReferralBonus()
    # Create a chain-like graph with 200 users
    for i in range(1, 200):
        sim.give_referral(f"User{i}", f"User{i+1}")
    return sim


def test_target_met_with_zero_bonus(small_network):
    """If adoption_prob always returns 1.0, bonus should be 0."""
    def adoption_prob(bonus):
        return 1.0

    random.seed(1)
    bonus = small_network.min_bonus_for_target(
        days=5, target_hires=5, adoption_probability=adoption_prob
    )
    assert bonus == 0


def test_target_already_met_by_initial_referrers(small_network):
    """If target <= initial_count, required bonus should be 0."""
    def adoption_prob(bonus):
        return 0.5  # arbitrary, shouldn't matter here

    random.seed(1)
    bonus = small_network.min_bonus_for_target(
        days=5, target_hires=5, adoption_probability=adoption_prob
    )
    assert bonus == 0


def test_bonus_calculation_reasonable(small_network):
    """Bonus should be reasonable for moderate adoption probability."""
    def adoption_prob(bonus):
        return min(0.2 + (bonus / 500.0), 1.0)

    random.seed(1)
    bonus = small_network.min_bonus_for_target(
        days=5, target_hires=8, adoption_probability=adoption_prob
    )
    assert isinstance(bonus, int)
    assert bonus % 10 == 0  # Should be rounded to nearest 10
    assert bonus >= 0


def test_large_network_bonus(large_network):
    """Large network should still compute a bonus."""
    def adoption_prob(bonus):
        return min(0.3 + (bonus / 1000.0), 1.0)

    random.seed(1)
    bonus = large_network.min_bonus_for_target(
        days=5, target_hires=50, adoption_probability=adoption_prob
    )
    assert isinstance(bonus, int)
    assert bonus % 10 == 0
    assert bonus >= 0


def test_probability_function_effect(small_network):
    """Higher adoption probability should require less bonus."""
    def low_adoption(bonus):
        return 0.2

    def high_adoption(bonus):
        return 0.9

    random.seed(1)
    low_bonus = small_network.min_bonus_for_target(
        days=5, target_hires=8, adoption_probability=low_adoption
    )
    high_bonus = small_network.min_bonus_for_target(
        days=5, target_hires=8, adoption_probability=high_adoption
    )
    assert high_bonus <= low_bonus
