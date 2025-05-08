from typing import List

class GoalDriftDetector:
    def __init__(self, original_goal: str):
        self.original_goal = original_goal
        self.goal_history = [original_goal]

    def check_drift(self, current_reasoning: str) -> float:
        """
        Simulates measuring semantic drift between the original goal 
        and the current reasoning path.
        """
        # Mock logic: longer reasoning chains tend to drift 
        drift = len(self.goal_history) * 0.02
        print(f"[DriftDetector] Estimated drift: {drift:.2f}")
        return min(drift, 1.0)

    def record_step(self, reasoning: str):
        self.goal_history.append(reasoning)
