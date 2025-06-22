from enum import Enum, auto
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
import uuid
import datetime

class AgentStatus(Enum):
    IDLE = auto()
    PLANNING = auto()
    EXECUTING = auto()
    WAITING_APPROVAL = auto()
    FAILED = auto()
    COMPLETED = auto()

@dataclass
class AgentState:
    agent_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: AgentStatus = AgentStatus.IDLE
    current_task: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict[str, Any]] = field(default_factory=list)
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = field(default_factory=datetime.datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "status": self.status.name,
            "current_task": self.current_task,
            "context": self.context,
            "history": self.history,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentState':
        return cls(
            agent_id=data["agent_id"],
            status=AgentStatus[data["status"]],
            current_task=data["current_task"],
            context=data["context"],
            history=data["history"],
            created_at=datetime.datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.datetime.fromisoformat(data["updated_at"])
        )

class BaseAgent:
    def __init__(self, state: Optional[AgentState] = None, memory: Any = None):
        self.state = state or AgentState()
        self.memory = memory

    def transition_to(self, new_status: AgentStatus):
        print(f"[Agent {self.state.agent_id}] Transitioning: {self.state.status.name} -> {new_status.name}")
        self.state.status = new_status
        self.state.updated_at = datetime.datetime.now()
        self.state.history.append({
            "timestamp": self.state.updated_at.isoformat(),
            "event": "transition",
            "from": self.state.status.name,
            "to": new_status.name
        })

    def run(self, task: str):
        self.state.current_task = task
        self.transition_to(AgentStatus.PLANNING)
        try:
            plan = self.plan(task)
            self.transition_to(AgentStatus.EXECUTING)
            result = self.execute(plan)
            self.transition_to(AgentStatus.COMPLETED)
            return result
        except Exception as e:
            print(f"Error during execution: {e}")
            self.transition_to(AgentStatus.FAILED)
            raise e

    def plan(self, task: str) -> List[Any]:
        """Override in subclasses"""
        return []

    def execute(self, plan: List[Any]) -> Any:
        """Override in subclasses"""
        return "Task completed"
