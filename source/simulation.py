import random
from collections import deque
from source.influencers import Influencers

class IncentiveSimulation(Influencers):
    def __init__(self):
        super().__init__()
        self.initial_count = 100
        self.referral_capacity = 10
        
    def simulate(self, probability, days):
        if not self.graph:
            return [0]*(days+1)
        
        starters = random.sample(list(self.graph.keys()), min(self.initial_count, len(self.graph)))
        influenced = set(starters)
        queue = deque(starters)
        capacity = {u: self.referral_capacity for u in self.graph.keys()}
        
        cumulative_referrals = [len(influenced)]
        
        for day in range(1, days+1):
            for _ in range(len(queue)):
                current = queue.popleft()
                for candidate in self.graph.get(current, []):
                    if candidate not in influenced and capacity[current]>0:
                        if random.random() <= probability:
                            influenced.add(candidate)
                            queue.append(candidate)
                            capacity[current]-=1
            cumulative_referrals.append(len(influenced))
        
        return cumulative_referrals

    def days_to_target(self, probability, target_total):
        if not self.graph:
            return 0
        
        total_nodes = len(self.graph)
        if target_total > total_nodes:
            return -1  
        
        if target_total <= self.initial_count:
            return 0
        
        starters = random.sample(list(self.graph.keys()), min(self.initial_count, len(self.graph)))
        influenced = set(starters)
        if len(influenced) >= target_total:
            return 0 

        max_days = len(self.graph) * self.referral_capacity
        queue = deque(starters)
        capacity = {u: self.referral_capacity for u in self.graph.keys()}
    
        day = 0
        while queue and len(influenced) < target_total and day < max_days:
            day += 1
            for _ in range(len(queue)):
                current = queue.popleft()
                for candidate in self.graph.get(current, []):
                    if candidate not in influenced and capacity[current] > 0:
                        if random.random() <= probability:
                            influenced.add(candidate)
                            queue.append(candidate)
                            capacity[current] -= 1
    
        return day if len(influenced) >= target_total else -1


