import time
from typing import List, Dict, Any

class StabilityMonitor:
    def __init__(self):
        self.coherence_scores: List[float] = []
        self.latencies: List[float] = []
        self.start_time = time.time()

    def record_step(self, coherence: float, latency: float):
        """
        Records the 'stability' of a single agent step.
        Coherence: A metric (0-1) representing reasoning consistency.
        Latency: Time taken for the step.
        """
        self.coherence_scores.append(coherence)
        self.latencies.append(latency)

    def get_drift_velocity(self) -> float:
        """
        Calculates how fast the agent's coherence is dropping.
        """
        if len(self.coherence_scores) < 2:
            return 0.0
        
        # Simple derivative of coherence over steps
        return self.coherence_scores[0] - self.coherence_scores[-1]

    def get_summary(self) -> Dict[str, Any]:
        return {
            "avg_coherence": sum(self.coherence_scores) / len(self.coherence_scores) if self.coherence_scores else 0,
            "total_steps": len(self.coherence_scores),
            "drift_velocity": self.get_drift_velocity(),
            "uptime": time.time() - self.start_time
        }
