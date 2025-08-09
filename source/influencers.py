from collections import deque
from source.reach import Reach

class Influencers(Reach):
    def compute_all_sets(self):
        reach_sets = {}
        for user in self.graph.keys():
            visited = set()
            queue = deque(self.graph.get(user, []))
            
            while queue:
                current =  queue.popleft()
                if current not in visited:
                    visited.add(current)
                    queue.extend(self.graph.get(current, []))
            
            reach_sets[user] = visited
        
        return reach_sets
    
    def unique_expansion(self):
        reach_sets = self.compute_all_sets()
        covered = set()
        influencers = []
        
        while True:
            best_user = None
            best_new = 0
            
            for user, reach in reach_sets.items():
                new_users = len(reach - covered)
                if new_users > best_new:
                    best_new = new_users
                    best_user = user
                    
            if best_user is None:
                break
            
            influencers.append(best_user)
            covered |= (reach_sets[best_user])
            
        return influencers
    
    def bfs_distances(self, start):
        distances = {u:float('inf') for u in self.graph.keys()}
        distances[start] = 0
        queue = deque([start])
        
        while queue:
            current = queue.popleft()
            for neighbor in self.graph.get(current, []):
                if distances[neighbor] == float('inf'):
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)
        
        return distances
    
    def flow_centrality(self):
        distance = {u: self.bfs_distances(u) for u in self.graph.keys()}
        scores = {u: 0 for u in self.graph.keys()}
        
        for s in self.graph.keys():
            for t in self.graph.keys():
                if s != t:
                    for v in self.graph.keys():
                        if (
                            v != s and v != t and
                            distance[s][v] != float('inf') and
                            distance[v][t] != float('inf') and
                            distance[s][t] != float('inf') and
                            distance[s][v] + distance[v][t] == distance[s][t]
                    ):
                            scores[v] += 1
        
        return sorted(scores.items(), key=lambda x: (-x[1], x[0]))
    
    
if __name__ == "__main__":
    inf = Influencers()
    inf.give_referral("Alice", "Bob")
    inf.give_referral("Alice", "Charlie")
    inf.give_referral("Bob", "David")
    inf.give_referral("Charlie", "Eve")

    print("Unique Reach Expansion:", inf.unique_expansion())
    print("Flow Centrality:", inf.flow_centrality())
