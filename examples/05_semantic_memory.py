from src.core.agent import BaseAgent
from src.memory.semantic import SemanticMemory, LessonLearned
import time

class KnowledgeableAgent(BaseAgent):
    def plan(self, task: str):
        print(f"[Agent] Planning for task: {task}")
        # Retrieve relevant lessons before planning
        lessons = []
        if self.memory:
            lessons = self.memory.retrieve_relevant(task)
            for lesson in lessons:
                print(f"[Agent] Retrieved lesson from memory: {lesson['content']}")
        
        if any("fail" in l['content'].lower() for l in lessons):
            print("[Agent] Adjusting plan based on past failures...")
            return ["Safe Action A", "Safe Action B"]
        
        return ["Action 1", "Action 2"]

def main():
    memory = SemanticMemory("test_memory.db")
    
    # 1. First run - agent fails
    print("--- FIRST RUN (FAILING) ---")
    agent = KnowledgeableAgent(memory=memory)
    
    # Simulate a failure and record it
    failure_msg = LessonLearned.format_failure(
        "Deploy Database", 
        "Root access denied", 
        "Use service account instead of root"
    )
    memory.add_memory(failure_msg, tags=["database", "deploy", "security"])
    
    # 2. Second run - agent remembers
    print("\n--- SECOND RUN (REMEMBERING) ---")
    agent2 = KnowledgeableAgent(memory=memory)
    plan = agent2.plan("Deploy Database")
    print(f"Final Plan: {plan}")

if __name__ == "__main__":
    main()
