import math
from dataclasses import dataclass
from typing import List

@dataclass
class AutonomyEnvelop:
    """
    Defines the 'safe' operating zone for an agent.
    As execution chain length increases, confidence decays.
    """
    base_confidence: float = 1.0
    decay_rate: float = 0.05
    min_threshold: float = 0.7

    def calculate_confidence(self, step_count: int) -> float:
        # Simple exponential decay: base * (1 - rate)^steps
        conf = self.base_confidence * math.pow(1 - self.decay_rate, step_count)
        return max(conf, 0.0)

    def is_within_envelope(self, step_count: int) -> bool:
        return self.calculate_confidence(step_count) >= self.min_threshold

class EnvelopeMonitor:
    def __init__(self, envelope: AutonomyEnvelop):
        self.envelope = envelope
        self.current_steps = 0

    def step(self):
        self.current_steps += 1
        conf = self.envelope.calculate_confidence(self.current_steps)
        if conf < self.envelope.min_threshold:
            print(f"[Envelope] WARNING: Confidence {conf:.2f} is below safety threshold!")
            return False
        return True
