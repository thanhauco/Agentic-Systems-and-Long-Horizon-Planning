from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class CostEstimate:
    input_tokens: int = 0
    output_tokens: int = 0
    tool_calls: int = 0
    
    # Rates per 1k tokens (simulated)
    input_rate: float = 0.015
    output_rate: float = 0.06
    tool_rate: float = 0.01

    def calculate_total(self) -> float:
        input_cost = (self.input_tokens / 1000) * self.input_rate
        output_cost = (self.output_tokens / 1000) * self.output_rate
        tool_cost = self.tool_calls * self.tool_rate
        return input_cost + output_cost + tool_cost

class CostTracker:
    def __init__(self, budget_limit: float = 10.0):
        self.total_spent = 0.0
        self.budget_limit = budget_limit
        self.history = []

    def record_transaction(self, estimate: CostEstimate):
        cost = estimate.calculate_total()
        self.total_spent += cost
        self.history.append({
            "cost": cost,
            "total_spent": self.total_spent
        })
        print(f"[Finance] Transaction recorded: ${cost:.4f}. Total: ${self.total_spent:.4f}")

    def is_within_budget(self, additional_cost: float = 0.0) -> bool:
        return (self.total_spent + additional_cost) <= self.budget_limit

    def get_remaining_budget(self) -> float:
        return max(0.0, self.budget_limit - self.total_spent)
