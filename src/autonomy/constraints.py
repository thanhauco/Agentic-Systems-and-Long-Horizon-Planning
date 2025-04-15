from dataclasses import dataclass
from typing import List, Any, Dict

@dataclass
class Constraint:
    name: str
    description: str
    is_hard: bool = True

class ConstraintEngine:
    def __init__(self):
        self.constraints: List[Constraint] = []

    def add_constraint(self, constraint: Constraint):
        self.constraints.append(constraint)

    def check_action(self, action_name: str, context: Dict[str, Any]) -> bool:
        """
        Mock constraint checking. 
        Example: Don't allow 'delete' actions on production data.
        """
        print(f"[ConstraintEngine] Checking action: {action_name}")
        
        # Hardcoded mock constraints
        if action_name == "delete_database" and context.get("env") == "prod":
            print("[ConstraintEngine] VIOLATION: Cannot delete production database!")
            return False
            
        return True
