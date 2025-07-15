from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
import datetime
import json

@dataclass
class ReasoningStep:
    thought: str
    action: str
    observation: str
    confidence: float
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

class ReasoningTrace:
    def __init__(self):
        self.steps: List[ReasoningStep] = []

    def add_step(self, thought: str, action: str, observation: str, confidence: float, **kwargs):
        step = ReasoningStep(
            thought=thought,
            action=action,
            observation=observation,
            confidence=confidence,
            metadata=kwargs
        )
        self.steps.append(step)
        print(f"[Trace] Step added: {action} (Confidence: {confidence:.2f})")

    def get_full_trace(self) -> List[Dict[str, Any]]:
        return [asdict(step) for step in self.steps]

    def export_json(self, filepath: str):
        with open(filepath, 'w') as f:
            json.dump(self.get_full_trace(), f, indent=2)
        print(f"[Trace] Exported trace to {filepath}")

    def analyze_stability(self) -> Dict[str, Any]:
        if not self.steps:
            return {"status": "empty"}
        
        confidences = [s.confidence for s in self.steps]
        avg_conf = sum(confidences) / len(confidences)
        drift = self.steps[0].confidence - self.steps[-1].confidence
        
        return {
            "avg_confidence": avg_conf,
            "drift": drift,
            "is_stable": drift < 0.3 and avg_conf > 0.7
        }
