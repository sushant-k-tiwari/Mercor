import pytest
from source.reach import Reach

def setup_sample_network():
    """
    Creates a sample referral network:
    Alice -> Bob, Charlie
    Bob -> David
    Charlie -> Eve
    Eve -> Frank
    """
    r = Reach()
    r.give_referral("Alice", "Bob")
    r.give_referral("Alice", "Charlie")
    r.give_referral("Bob", "David")
    r.give_referral("Charlie", "Eve")
    r.give_referral("Eve", "Frank")
    return r

def test_total_reach_basic():
    r = setup_sample_network()
    assert r.total_reach("Alice") == 5   # Bob, Charlie, David, Eve, Frank
    assert r.total_reach("Bob") == 1     # David
    assert r.total_reach("Charlie") == 2 # Eve, Frank
    assert r.total_reach("David") == 0   # No referrals

def test_k_percentile_90():
    r = setup_sample_network()
    k = r.k_percentile(90)
    # Only Alice should be above the 90th percentile in this small network
    assert k == 1

def test_k_percentile_50():
    r = setup_sample_network()
    k = r.k_percentile(50)
    # Half the users should be in the top 50% by reach
    assert k >= 1

def test_top_k_referrers_fixed_k():
    r = setup_sample_network()
    top_2 = r.top_k_referrers(k=2)
    assert top_2[0][0] == "Alice"
    assert top_2[0][1] == 5
    assert len(top_2) == 2

def test_top_k_referrers_percentile():
    r = setup_sample_network()
    top_users = r.top_k_referrers(percentile=80)
    # Should return all users above 80th percentile reach
    assert top_users[0][0] == "Alice"
    assert all(top_users[i][1] >= top_users[-1][1] for i in range(len(top_users)))
