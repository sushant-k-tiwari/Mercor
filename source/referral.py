class Referrals:
    def __init__(self):
        self.graph = {}
        self.referred = {}
        
        
    def give_referral(self, referrer, candidate):
        if referrer not in self.graph:
            self.graph[referrer] = set()
        if candidate not in self.graph:
            self.graph[candidate] = set()
        
        if referrer == candidate:
            print("Error: You cannot refer yourself.")
            return
        
        if candidate in self.referred:
            print(f"Error: {candidate} has already been referred.")
            return
        
        visited = set()
        if self.check_cycle(candidate, referrer, visited):
            print("Error: There is a cycle in the referral network.")
            return
        
        self.graph[referrer].add(candidate)
        self.referred[candidate] = referrer
        
    def check_cycle(self, candidate, referrer, visited):
        if candidate == referrer:
            return True
        visited.add(candidate)
        for neighbor in self.graph.get(candidate, []):
            if neighbor not in visited and self.check_cycle(neighbor, referrer, visited):
                return True
        return False
    
    def get_referrals(self, user):
        if user in self.graph:
            return self.graph[user]
        else:
            return set()
        

# if __name__ == "__main__":
#     rg = Referrals()
#     rg.give_referral("Alice", "Bob")
#     rg.give_referral("Alice", "Charlie")
#     rg.give_referral("Bob", "David")
#     rg.give_referral(  "Charlie","David")  # Should give cycle error

#     print(rg.get_referrals("Alice"))  # {'Bob', 'Charlie'}
