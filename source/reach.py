from collections import deque
from source.referral import Referrals

class Reach(Referrals):
    def total_reach(self, user):
        visited = set()
        queue = deque(self.graph.get(user, []))
        
        while queue:
            current = queue.popleft()
            if current not in visited:
                visited.add(current)
                queue.extend(self.graph.get(current, []))
        
        return len(visited)
    
    def top_k_referrers(self, k):
        reach_count = []
        for user in self.graph.keys():
            count = self.total_reach(user)
            reach_count.append((user, count))
        
        reach_count.sort(key=lambda x: (-x[1], x[0]))
        
        return reach_count[:k]
    
    
if __name__ == "__main__":
    ra = Reach()
    ra.give_referral("Alice", "Bob")
    ra.give_referral("Alice", "Charlie")
    ra.give_referral("Bob", "David")
    ra.give_referral("Charlie", "Eve")

    print("Total reach of Alice:", ra.total_reach("Alice"))  # 4
    print("Top 2 referrers:", ra.top_k_referrers(2))
