from typing import Optional, Any, Callable
from ..core.decision import DecisionPoint

class InterventionManager:
    def __init__(self, ui_callback: Optional[Callable[[DecisionPoint], Any]] = None):
        self.ui_callback = ui_callback
        self.intervention_history = []

    def request_human_help(self, decision: DecisionPoint) -> Any:
        """
        Pauses agent execution and waits for human input.
        """
        print(f"\n[INTERVENTION] Human help required for: {decision.description}")
        print(f"Reason: {decision.reasoning}")
        
        if self.ui_callback:
            response = self.ui_callback(decision)
        else:
            # Fallback to CLI input
            print("Action required: (a)pprove, (r)eject, (p)rovide fix")
            response = input("> ").strip().lower()

        self.intervention_history.append({
            "decision_id": decision.id,
            "response": response
        })
        
        return response

    def was_interrupted(self) -> bool:
        return len(self.intervention_history) > 0
