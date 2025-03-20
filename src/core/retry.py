import time
import random
from enum import Enum, auto
from dataclasses import dataclass
from typing import Callable, Any, Optional

class CircuitState(Enum):
    CLOSED = auto()
    OPEN = auto()
    HALF_OPEN = auto()

@dataclass
class RetryPolicy:
    max_attempts: int = 3
    backoff_factor: float = 2.0
    jitter: bool = True

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = CircuitState.CLOSED
        self.failures = 0
        self.last_failure_time: Optional[float] = None

    def record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            print("[CircuitBreaker] Opening circuit...")
            self.state = CircuitState.OPEN

    def record_success(self):
        self.failures = 0
        self.state = CircuitState.CLOSED

    def can_execute(self) -> bool:
        if self.state == CircuitState.CLOSED:
            return True
        
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                print("[CircuitBreaker] Entering Half-Open state...")
                self.state = CircuitState.HALF_OPEN
                return True
            return False
            
        return True # Half-open

def retry_with_backoff(policy: RetryPolicy, circuit_breaker: Optional[CircuitBreaker] = None):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            if circuit_breaker and not circuit_breaker.can_execute():
                raise Exception("Circuit is OPEN. Execution halted.")

            attempts = 0
            while attempts < policy.max_attempts:
                try:
                    result = func(*args, **kwargs)
                    if circuit_breaker:
                        circuit_breaker.record_success()
                    return result
                except Exception as e:
                    attempts += 1
                    if attempts == policy.max_attempts:
                        if circuit_breaker:
                            circuit_breaker.record_failure()
                        raise e
                    
                    wait_time = policy.backoff_factor ** attempts
                    if policy.jitter:
                        wait_time += random.uniform(0, 1)
                    
                    print(f"[Retry] Attempt {attempts} failed: {e}. Retrying in {wait_time:.2f}s...")
                    time.sleep(wait_time)
        return wrapper
    return decorator
