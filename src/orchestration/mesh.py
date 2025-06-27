from typing import List, Dict, Any
from ..core.agent import BaseAgent, AgentStatus

class Orchestrator:
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}

    def register_agent(self, name: str, agent: BaseAgent):
        self.agents[name] = agent
        print(f"[Orchestrator] Registered agent: {name}")

    def delegate(self, target_agent_name: str, task: str) -> Any:
        if target_agent_name not in self.agents:
            raise ValueError(f"Agent {target_agent_name} not found")
        
        print(f"[Orchestrator] Delegating task to {target_agent_name}: {task}")
        return self.agents[target_agent_name].run(task)

class MultiAgentCoordinator(BaseAgent):
    def __init__(self, orchestrator: Orchestrator, **kwargs):
        super().__init__(**kwargs)
        self.orchestrator = orchestrator

    def plan(self, task: str) -> List[Dict[str, Any]]:
        print(f"[Coordinator] Breaking down multi-agent task: {task}")
        # Simulating workflow breakdown
        return [
            {"agent": "researcher", "task": f"Research about {task}"},
            {"agent": "writer", "task": f"Write report based on research for {task}"}
        ]

    def execute(self, plan: List[Dict[str, Any]]) -> str:
        results = []
        for step in plan:
            res = self.orchestrator.delegate(step["agent"], step["task"])
            results.append(res)
        return "\n".join(results)
