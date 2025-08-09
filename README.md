# Mercor Referral Network Challenge

### **Part 1 – Referral Graph**

- **Data Structure:**

  - Chose a **dictionary of sets** (`dict[str, set[str]]`) to store referrals given to candidates.
  - Each key = a user and value = set of candidates they have referred.

- **Constraints Handling:**

  1. **No Self-Referrals:** Prevented the self referrals by direct check before insertion **i.e.** referrer != candidate.

  2. **Unique Referrer:** `self.referred` dictionay ensures that each candidate is referred only once in the graph.

  3. **Acyclic Graph:** Cycle detection is done using DFS : `check_cycle` method before adding an edge. This ensures that the graph is acyclic.

  4. **Why not BFS:** BFS is not suitable for acyclic graphs because it may visit nodes that are not reachable from the root and it may detect a false positive cycle.

- **Why Dictionaries:** Dictionaries and sets give **O(1)** average complexity for insertions and lookups, making operations fast and efficient.

---

### **Part 2 – Full Network Reach**

- Implemented **BFS traversal** to compute total reach (direct + indirect referrals) for each user in the network graph.

- `top_k_referrers` ranks users by total reach and returns the top `k` users with the highest reach.

- **Choosing k:**

  - Caller can pass `k` directly for fixed rankings, or use `percentile` to select top influencers based on reach distribution.

- **Why Percentile:** Allows for flexible k selection based on reach distribution and it ensures:

  - **Fairness:** Instead of a fixed number of top referrers, we reward everyone performing above a certain level.

  - **Business Value:** One can set thresholds for bonus programs by percentile.

- **Why BFS:** Guarantees shortest-path order, avoids repeated counting of already visited nodes.

---

### **Part 3 – Identify Influencers**

Two metrics implemented:

1. **Unique Reach Expansion:**

   - Greedy algorithm for selecting users who added the most _new_ candidates to coverage.

   - Great for marketing campaigns where minimizing audience overlap matters most.

2. **Flow Centrality:**

   - Computes shortest-path distances between all user pairs using BFS starting from each user/node in the graph.

   - Then scoring users who appear most often on shortest paths to other users.

- **Metric Comparison & Use Cases:**
  | Metric | Best For | Business Scenario |
  |----------------------|----------|------------------|
  | **Reach** |Finding users with the highest reach | Creating a leaderboard to reward most connected individuals/referrers |
  | **Unique Reach** | Minimizing overlap and avoiding duplication | Can be used to select a lead candidate for campaigns or other programs to bring new people to the network |
  | **Flow Centrality** | Measuring importance for network stability | Identifying most significant influencers in the network and promoting them for retention |

---

### **Part 4 – Network Growth Simulation**

- Parameters:

  - **Initial Referrers:** 100
  - **Referral Capacity:** 10 per lifetime

- `simulate(probability, days)` returns cumulative referrals by day.
- `days_to_target(probability, target)` finds days to hit target hires using binary search.
- **Why Queues:** BFS-like propagation ensures correct day-by-day simulation of referrals.

---

### **Part 5 – Referral Bonus Optimization**

We use a function `adoption_probability(bonus)` that models the probability of a referral being made based on the bonus offered.

This function is **monotonically increasing** — higher bonuses never result in lower participation.

The optimization process involves **three main steps**:

1. **Check Extreme Cases**

   - **Bonus = $0:** If target hires can already be reached without offering any bonus, return **0**.
   - **Bonus = $10,000:** If even this bonus cannot achieve the target, return **None** (unreachable).

2. **Binary Search for the Minimum Bonus**

   - Search between `$0` and `$10,000`, halving the range each time.
   - At each midpoint:
     - Convert bonus → probability via `adoption_probability(mid)`.
     - Run the **Part 4 Simulation** to check hires achieved.
     - Adjust the search bounds depending on whether the target was met.

3. **Return Final Bonus**
   - If target is met, round **up** to the nearest $10.
   - If target is unreachable, return `None`.

---

### Time Complexity

- **Binary Search Iterations:**  
  Cuts range in half → **O(log(range / eps))** iterations.

  - `range` = 10,000 (max bonus considered)
  - `eps` = precision threshold (e.g., `1e-3`)

- **Per Iteration Cost:**  
  Runs a **BFS-based simulation** from Part 4: **O(simulation_time)**.

- **Overall Complexity:**  
  $O(log(range / eps) * simulation\_time)$

- **Why this is useful:**  
  This method ensures we don’t overpay bonuses while still meeting hiring goals, making it **cost-efficient**.

---

## Testing Strategy

- **Unit Tests:** Validate each part’s functionality independently.
- **Constraint Tests:** Check self-referrals, cycles, and duplicate referrals are rejected.
- **Edge Cases:**
  - Empty network.
  - Probability = 0 and 1.
  - Target ≤ initial referrers.
  - Unreachable targets.
- **Simulation Tests:** Deterministic runs with `random.seed` for reproducibility.

---

## AI and Other Sources Usage Acknowledgment

I used StackOverflow and Google to:

- To understand the difference between BFS and DFS usage for this challenge.

- When it is good to use BFS over DFS and vice versa.

- The broker concept from graph theory to understand the problem and concepts like cut vertex, bridge, etc.

I used **ChatGPT** to:

- Help brainstorm algorithmic approaches.
- Debug failing test cases.
- Generate boilerplate README structure.
- The code logic and final design choices were my own, and I used ChatGPT to improve them and design my test files for faster testing and debugging.
