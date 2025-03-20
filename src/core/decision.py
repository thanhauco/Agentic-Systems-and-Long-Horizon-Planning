from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, Callable, Any

class AutonomyLevel(Enum):
    FULL_AUTO = auto()    # AI makes all decisions
    SUPERVISED = auto()   # AI suggests, human approves
    MANUAL = auto()       # Human provides input at every step

@dataclass
class DecisionPoint:
    id: str
    description: str
    confidence: float
    reasoning: str
    autonomy_level: AutonomyLevel = AutonomyLevel.FULL_AUTO
    threshold: float = 0.8

class DecisionBoundary:
    def __init__(self, approval_callback: Optional[Callable[[DecisionPoint], bool]] = None):
        self.approval_callback = approval_callback

    def evaluate(self, decision: DecisionPoint) -> bool:
        print(f"[Decision] Evaluating: {decision.description} (Confidence: {decision.confidence:.2f})")
        
        if decision.autonomy_level == AutonomyLevel.MANUAL:
            return self._request_approval(decision)
        
        if decision.confidence < decision.threshold:
            print(f"[Decision] Confidence ({decision.confidence:.2f}) below threshold ({decision.threshold:.2f}). Escalating...")
            return self._request_approval(decision)
            
        if decision.autonomy_level == AutonomyLevel.SUPERVISED:
            return self._request_approval(decision)
            
        return True

    def _request_approval(self, decision: DecisionPoint) -> bool:
        if self.approval_callback:
            return self.approval_callback(decision)
        
        print(f"[Decision] NO APPROVAL CALLBACK. Defaulting to BLOCK for decision: {decision.id}")
        return False
