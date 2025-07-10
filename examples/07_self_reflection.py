from src.core.agent import BaseAgent
from src.reflection.engine import SelfCorrectingAgentMixin
import time

class ReflectiveAgent(BaseAgent, SelfCorrectingAgentMixin):
    def plan(self, task: str):
        return ["Action 1", "Action 2", "Action 3", "Action 4", "Action 5", "Action 6"]

    def execute(self, plan):
        for i, action in enumerate(plan):
            print(f"Executing: {action}")
            # Every 3 steps, perform reflection
            if (i + 1) % 3 == 0:
                self.perform_reflection()
            time.sleep(0.2)
        return "Complete"

def main():
    agent = ReflectiveAgent()
    print("--- STARTING REFLECTIVE AGENT ---")
    agent.run("Complex long-running operation")

if __name__ == "__main__":
    main()
