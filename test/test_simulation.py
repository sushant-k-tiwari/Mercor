import random
import pytest
from source.simulation import IncentiveSimulation


@pytest.fixture
def empty_network():
    return IncentiveSimulation()


@pytest.fixture
def small_network():
    sim = IncentiveSimulation()
    sim.initial_count = 1  # start small to test spread
    sim.give_referral("A", "B")
    sim.give_referral("B", "C")
    sim.give_referral("C", "D")
    sim.give_referral("D", "E")
    return sim


@pytest.fixture
def large_network():
    sim = IncentiveSimulation()
    sim.initial_count = 100
    num_nodes = 200
    # Build a simple acyclic network
    for i in range(1, num_nodes):
        for j in range(1, 4):
            target = i + j
            if target <= num_nodes:
                sim.give_referral(f"User{i}", f"User{target}")
    return sim


def test_simulate_empty_graph(empty_network):
    result = empty_network.simulate(probability=1.0, days=5)
    assert result == [0] * 6  # days + 1
    assert isinstance(result, list)


def test_days_to_target_empty_graph(empty_network):
    days_needed = empty_network.days_to_target(probability=1.0, target_total=5)
    assert days_needed == 0  # nothing to spread


def test_simulate_small_network(small_network):
    random.seed(1)
    result = small_network.simulate(probability=1.0, days=5)
    assert isinstance(result, list)
    assert result[0] == 1  # start with 1 active
    assert result[-1] >= result[0]
    assert len(result) == 6  # days + 1


def test_days_to_target_small_network(small_network):
    random.seed(1)
    days_needed = small_network.days_to_target(probability=1.0, target_total=5)
    assert isinstance(days_needed, int)
    if days_needed == -1:  # unreachable
        assert 5 >= len(small_network.graph)  # sanity check: asking for more than exists
    else:
        assert days_needed > 0



def test_large_network_100_active_referrers(large_network):
    random.seed(1)
    result = large_network.simulate(probability=1.0, days=10)
    assert result[0] == min(large_network.initial_count, len(large_network.graph))
    assert result[-1] >= result[0]
    assert len(result) == 11  # days + 1

    # If target <= initial_count, should be 0 days
    days_needed_small_target = large_network.days_to_target(probability=1.0, target_total=50)
    assert days_needed_small_target == 0

    # Larger target, should require spreading
    days_needed_big_target = large_network.days_to_target(probability=1.0, target_total=150)
    assert days_needed_big_target > 0


def test_unreachable_target(large_network):
    random.seed(1)
    # Probability 0 => no spread
    days_needed = large_network.days_to_target(probability=0.0, target_total=300)
    assert days_needed == -1  # impossible to reach
