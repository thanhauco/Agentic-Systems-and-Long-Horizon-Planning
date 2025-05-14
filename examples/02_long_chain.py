from src.planning.decomposition import TaskDecomposer, TaskGraph
from src.planning.checkpoint import CheckpointManager
import time

def main():
    decomposer = TaskDecomposer()
    checkpointer = CheckpointManager()
    
    # 1. Decompose a long goal
    goal = "Build a sustainable city on Mars"
    tasks = decomposer.decompose(goal)
    graph = TaskGraph(tasks)
    
    # 2. Execute steps and checkpoint
    print("\nStarting execution chain...")
    for i in range(len(tasks)):
        ready = graph.get_ready_tasks()
        if not ready: break
        
        current_task = ready[0]
        print(f"Step {i+1}: Executing '{current_task.description}'")
        
        # Simulate work
        time.sleep(0.3)
        graph.update_task_status(current_task.id, "COMPLETED", {"status": "ok"})
        
        # Create checkpoint
        checkpointer.create_checkpoint(graph, {"last_task": current_task.id})

    print("\nChain complete. Final Checkpoints:", len(checkpointer.history))

if __name__ == "__main__":
    main()
