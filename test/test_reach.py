import pytest
from source.reach import Reach

def setup_sample_network():
    """
    Creates a sample referral network:
    Alice -> Bob, Charlie
    Bob -> David
    Charlie -> Eve
    """
    ra = Reach()
    ra.give_referral("Alice", "Bob")
    ra.give_referral("Alice", "Charlie")
    ra.give_referral("Bob", "David")
    ra.give_referral("Charlie", "Eve")
    return ra

def test_total_reach_simple():
    ra = setup_sample_network()
    assert ra.total_reach("Alice") == 4   # Bob, Charlie, David, Eve
    assert ra.total_reach("Bob") == 1     # David
    assert ra.total_reach("Charlie") == 1 # Eve

def test_total_reach_no_referrals():
    ra = setup_sample_network()
    assert ra.total_reach("David") == 0   # David referred no one

def test_top_k_referrers():
    ra = setup_sample_network()
    top_2 = ra.top_k_referrers(2)
    # Top should be Alice first (reach 4), then Bob or Charlie (reach 1)
    assert top_2[0][0] == "Alice"
    assert top_2[0][1] == 4
    assert top_2[1][1] == 1

def test_top_k_ties():
    ra = Reach()
    ra.give_referral("A", "B")
    ra.give_referral("C", "D")
    top_2 = ra.top_k_referrers(2)
    # Both A and C have reach 1, sorted alphabetically
    assert top_2 == [("A", 1), ("C", 1)]
