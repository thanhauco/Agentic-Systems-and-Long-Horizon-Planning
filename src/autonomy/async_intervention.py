import uuid
from typing import Dict, Any, Optional
from ..core.agent import AgentStatus

class AsyncIntervention:
    """
    Manages long-running human-in-the-loop tasks that don't block the execution process.
    """
    def __init__(self, state_store: Any):
        self.state_store = state_store
        self.active_requests: Dict[str, Dict[str, Any]] = {}

    def suspend_for_human(self, agent_state: Any, reason: str) -> str:
        request_id = str(uuid.uuid4())
        print(f"[AsyncIntervention] SUSPENDING AGENT {agent_state.agent_id}. Request ID: {request_id}")
        
        # Change status to WAITING_APPROVAL
        agent_state.status = AgentStatus.WAITING_APPROVAL
        self.active_requests[request_id] = {
            "agent_id": agent_state.agent_id,
            "reason": reason,
            "status": "pending"
        }
        
        # Persist the suspended state
        self.state_store.save_state(agent_state)
        return request_id

    def resolve_request(self, request_id: str, feedback: Any) -> bool:
        if request_id not in self.active_requests:
            return False
            
        request = self.active_requests[request_id]
        agent_id = request["agent_id"]
        
        print(f"[AsyncIntervention] RESOLVING request {request_id} for agent {agent_id}")
        
        # Load the agent back
        state = self.state_store.load_state(agent_id)
        if not state:
            return False
            
        state.status = AgentStatus.EXECUTING
        state.context["human_feedback"] = feedback
        
        # Save the resumed state
        self.state_store.save_state(state)
        del self.active_requests[request_id]
        return True
