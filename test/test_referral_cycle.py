import pytest
from source.referral import Referrals

def test_add_referral_success():
    rg = Referrals()
    rg.give_referral("Alice", "Bob")
    assert "Bob" in rg.get_referrals("Alice")

def test_no_self_referral(capsys):
    rg = Referrals()
    rg.give_referral("Alice", "Alice")
    captured = capsys.readouterr()
    assert "cannot refer yourself" in captured.out.lower()
    assert "Alice" not in rg.get_referrals("Alice")

def test_unique_referrer(capsys):
    rg = Referrals()
    rg.give_referral("Alice", "Bob")
    rg.give_referral("Charlie", "Bob")  # should print error
    captured = capsys.readouterr()
    assert "already been referred" in captured.out.lower()
    assert rg.referred["Bob"] == "Alice"

def test_no_cycles(capsys):
    rg = Referrals()
    rg.give_referral("Alice", "Bob")
    rg.give_referral("Bob", "Charlie")
    rg.give_referral("Charlie", "Alice")  # should print cycle error
    captured = capsys.readouterr()
    assert "cycle" in captured.out.lower()
    assert "Alice" not in rg.get_referrals("Charlie")

def test_get_referrals_empty():
    rg = Referrals()
    assert rg.get_referrals("UnknownUser") == set()
