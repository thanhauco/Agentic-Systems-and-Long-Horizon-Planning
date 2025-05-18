from src.autonomy.envelope import AutonomyEnvelop, EnvelopeMonitor
from src.core.decision import DecisionBoundary, DecisionPoint, AutonomyLevel
import time

def main():
    envelope = AutonomyEnvelop(base_confidence=1.0, decay_rate=0.1, min_threshold=0.6)
    monitor = EnvelopeMonitor(envelope)
    boundary = DecisionBoundary()
    
    print("Simulating execution until autonomy envelope breach...")
    
    for step in range(1, 10):
        print(f"\n--- Step {step} ---")
        is_safe = monitor.step()
        confidence = envelope.calculate_confidence(step)
        
        # Create a decision point based on current confidence
        dp = DecisionPoint(
            id=f"step_{step}",
            description=f"Action at step {step}",
            confidence=confidence,
            reasoning="Continuing long chain execution",
            threshold=0.7 # Higher than envelope threshold for early warning
        )
        
        allowed = boundary.evaluate(dp)
        
        if not allowed or not is_safe:
            print(">>> STOP: Autonomy boundary reached. Requires Human Intervention.")
            break
            
        time.sleep(0.4)

if __name__ == "__main__":
    main()
