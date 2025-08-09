import math
from source.simulation import IncentiveSimulation

class ReferralBonus(IncentiveSimulation):
    def min_bonus_for_target(self, days, target_hires, adoption_probability, eps=1e-3):
        # If target already achievable by initial referrers without any bonus
        if target_hires <= self.initial_count:
            return 0

        # Check extreme cases first
        prob_zero = adoption_probability(0)
        if self.simulate(prob_zero, days)[-1] >= target_hires:
            return 0  # Already achievable at zero bonus

        prob_high = adoption_probability(10000.0)
        if self.simulate(prob_high, days)[-1] < target_hires:
            return None  # Even huge bonus can't meet target

        # Binary search for minimum bonus
        low = 0.0
        high = 10000.0
        achievable = False

        while (high - low) > eps:
            mid = (high + low) / 2.0
            probability = adoption_probability(mid)
            hires = self.simulate(probability, days)[-1]

            if hires >= target_hires:
                high = mid
                achievable = True
            else:
                low = mid

        if not achievable:
            return None

        # Round up to nearest $10, but ensure 0 if high is essentially 0
        min_bonus = math.ceil(high / 10.0) * 10
        if min_bonus == 0:
            return 0
        return min_bonus
