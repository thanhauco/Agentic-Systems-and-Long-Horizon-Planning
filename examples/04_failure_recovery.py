from src.failure.recovery import RecoveryOrchestrator, RecoveryMode
from src.core.retry import retry_with_backoff, RetryPolicy
import random

# A flaky function to simulate tool failure
@retry_with_backoff(RetryPolicy(max_attempts=3, backoff_factor=0.1))
def call_external_api():
    if random.random() < 0.7:
        raise Exception("API Connection Timeout")
    return "API Success"

def main():
    orchestrator = RecoveryOrchestrator()
    
    print("Scenario 1: Transient Failure (Retry)")
    try:
        result = call_external_api()
        print("Result:", result)
    except Exception as e:
        print("Retry failed. Handing to orchestrator...")
        strategy = orchestrator.determine_strategy({"type": "transient", "severity": 5})
        orchestrator.execute_recovery(strategy)

    print("\nScenario 2: Critical Failure (Escalate)")
    strategy = orchestrator.determine_strategy({"type": "security_violation", "severity": 10})
    orchestrator.execute_recovery(strategy)

if __name__ == "__main__":
    main()
