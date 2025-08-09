import numpy as np
import math
from collections import deque
from source.referral import Referrals

class Reach(Referrals):
    
    def k_percentile(self, percentile = 90):
        if not self.graph:
            return 0
        reaches = [self.total_reach(user) for user in self.graph.keys()]
        threshold = np.percentile(reaches, percentile)
        return sum(1 for reach in reaches if reach >= threshold)
    
    def total_reach(self, user):
        visited = set()
        queue = deque(self.graph.get(user, []))
        
        while queue:
            current = queue.popleft()
            if current not in visited:
                visited.add(current)
                queue.extend(self.graph.get(current, []))
        
        return len(visited)
    
    def top_k_referrers(self, k=None, percentile=None):
        
        if percentile is not None:
            k = self.k_percentile(percentile)
        
        
        reach_count = []
        for user in self.graph.keys():
            count = self.total_reach(user)
            reach_count.append((user, count))
        
        reach_count.sort(key=lambda x: (-x[1], x[0]))
        
        return reach_count[:k]
    


