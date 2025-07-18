import pytest
import os
from src.core.agent import BaseAgent, AgentStatus, AgentState
from src.core.state import StateStore
from src.core.retry import RetryPolicy, retry_with_backoff, CircuitBreaker
from src.core.decision import DecisionPoint, DecisionBoundary, AutonomyLevel

def test_agent_status_transitions():
    agent = BaseAgent()
    assert agent.state.status == AgentStatus.IDLE
    
    agent.transition_to(AgentStatus.PLANNING)
    assert agent.state.status == AgentStatus.PLANNING
    assert len(agent.state.history) == 1

def test_state_persistence():
    db_name = "test_persistence.db"
    if os.path.exists(db_name):
        os.remove(db_name)
        
    store = StateStore(db_name)
    agent = BaseAgent()
    agent.state.current_task = "test task"
    
    store.save_state(agent.state)
    
    loaded_state = store.load_state(agent.state.agent_id)
    assert loaded_state.current_task == "test task"
    assert loaded_state.agent_id == agent.state.agent_id
    
    os.remove(db_name)

def test_circuit_breaker():
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=1)
    assert cb.can_execute() is True
    
    cb.record_failure()
    cb.record_failure()
    assert cb.can_execute() is False
    
def test_decision_boundary():
    def mock_approval(dp):
        return dp.id == "allowed"
        
    boundary = DecisionBoundary(approval_callback=mock_approval)
    
    dp_ok = DecisionPoint(id="allowed", description="test", confidence=0.5, reasoning="low conf")
    dp_fail = DecisionPoint(id="blocked", description="test", confidence=0.5, reasoning="low conf")
    
    assert boundary.evaluate(dp_ok) is True
    assert boundary.evaluate(dp_fail) is False
