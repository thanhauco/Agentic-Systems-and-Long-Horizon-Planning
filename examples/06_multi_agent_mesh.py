from src.core.agent import BaseAgent
from src.orchestration.mesh import Orchestrator, MultiAgentCoordinator

class SpecializedAgent(BaseAgent):
    def __init__(self, role: str, **kwargs):
        super().__init__(**kwargs)
        self.role = role

    def plan(self, task: str):
        return [f"{self.role} is performing: {task}"]

    def execute(self, plan):
        return f"Result from {self.role}: {plan[0]}"

def main():
    orchestrator = Orchestrator()
    
    # Register specialized agents
    orchestrator.register_agent("researcher", SpecializedAgent(role="Researcher"))
    orchestrator.register_agent("writer", SpecializedAgent(role="Writer"))
    
    # Create coordinator
    coordinator = MultiAgentCoordinator(orchestrator=orchestrator)
    
    print("\n--- STARTING MULTI-AGENT WORKFLOW ---")
    final_output = coordinator.run("Future of AI in 2030")
    
    print("\n--- FINAL OUTPUT ---")
    print(final_output)

if __name__ == "__main__":
    main()
