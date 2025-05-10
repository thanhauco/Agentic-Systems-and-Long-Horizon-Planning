from src.core.agent import BaseAgent, AgentStatus
from src.core.state import StateStore
import time

class SimpleAgent(BaseAgent):
    def plan(self, task: str):
        return ["Action 1", "Action 2", "Action 3"]

    def execute(self, plan):
        for action in plan:
            print(f"Executing: {action}")
            time.sleep(0.5)
        return "Done"

def main():
    # Initialize store
    store = StateStore("basic_agent.db")
    
    # Create agent
    agent = SimpleAgent()
    print(f"Agent ID: {agent.state.agent_id}")
    
    # Initial save
    store.save_state(agent.state)
    
    # Run task
    try:
        agent.run("Write a greeting")
        store.save_state(agent.state)
        print("Final Status:", agent.state.status.name)
    except Exception as e:
        store.save_state(agent.state)
        print("Execution failed.")

if __name__ == "__main__":
    main()
