import pytest
from source.influencers import Influencers

def setup_sample_network():
    """
    Creates a sample referral network:
    Alice -> Bob, Charlie
    Bob -> David
    Charlie -> Eve
    Eve -> Frank
    """
    inf = Influencers()
    inf.give_referral("Alice", "Bob")
    inf.give_referral("Alice", "Charlie")
    inf.give_referral("Bob", "David")
    inf.give_referral("Charlie", "Eve")
    inf.give_referral("Eve", "Frank")
    return inf

def test_compute_reach_sets():
    inf = setup_sample_network()
    reach_sets = inf.compute_all_sets()
    assert reach_sets["Alice"] == {"Bob", "Charlie", "David", "Eve", "Frank"}
    assert reach_sets["Bob"] == {"David"}
    assert reach_sets["Eve"] == {"Frank"}

def test_unique_reach_expansion():
    inf = setup_sample_network()
    influencers = inf.unique_expansion()
    # Alice should always be first because she reaches the most people
    assert influencers[0] == "Alice"
    # All influencers should be unique users
    assert len(influencers) == len(set(influencers))

def test_flow_centrality_scores():
    inf = setup_sample_network()
    scores = dict(inf.flow_centrality())
    # Alice is the originator, but Bob and Charlie are connectors
    assert scores["Alice"] >= 0
    assert scores["Bob"] > 0
    assert scores["Charlie"] > 0
    # Frank has no outgoing edges, should have low score
    assert scores["Frank"] == 0

def test_flow_centrality_ranking_order():
    inf = setup_sample_network()
    ranking = inf.flow_centrality()
    # Ranking should be sorted by score (desc), then name (asc)
    for i in range(len(ranking) - 1):
        score_i, score_next = ranking[i][1], ranking[i+1][1]
        name_i, name_next = ranking[i][0], ranking[i+1][0]
        if score_i == score_next:
            assert name_i < name_next
        else:
            assert score_i >= score_next
