from dataclasses import dataclass
from typing import List, Dict, Any, Callable
import re

@dataclass
class PolicyRule:
    name: str
    description: str
    validator: Callable[[Dict[str, Any]], bool]
    severity: str = "ERROR" # ERROR, WARNING

class PolicyEngine:
    """
    High-level governance layer. Policies are cross-cutting rules
    that apply to all agents and tools.
    """
    def __init__(self):
        self.rules: List[PolicyRule] = []

    def add_rule(self, rule: PolicyRule):
        self.rules.append(rule)

    def evaluate_intent(self, intent: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        violations = []
        print(f"[PolicyEngine] Evaluating intent: '{intent}'")
        
        for rule in self.rules:
            if not rule.validator({"intent": intent, "context": context}):
                violations.append({
                    "rule": rule.name,
                    "description": rule.description,
                    "severity": rule.severity
                })
        
        return violations

# Example Policy: No data exfiltration to unauthorized domains
def check_exfiltration(data: Dict[str, Any]) -> bool:
    intent = data.get("intent", "").lower()
    # Simple regex mock for url detection
    if "http" in intent and not "internal.corp" in intent:
        return False
    return True

# Example Policy: Budget limits
def check_budget(data: Dict[str, Any]) -> bool:
    context = data.get("context", {})
    cost = context.get("estimated_cost", 0)
    limit = context.get("budget_limit", 100)
    return cost <= limit
