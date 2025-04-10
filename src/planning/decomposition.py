from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import uuid

@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    dependencies: List[str] = field(default_factory=list)
    subtasks: List['Task'] = field(default_factory=list)
    status: str = "PENDING"  # PENDING, RUNNING, COMPLETED, FAILED
    result: Any = None

class TaskDecomposer:
    def decompose(self, goal: str) -> List[Task]:
        """
        Simulates decomposing a complex goal into a hierarchy of tasks.
        In a real system, this would call an LLM.
        """
        print(f"[Decomposer] Decomposing goal: {goal}")
        # Mock decomposition
        tasks = [
            Task(description="Research market trends", id="task_1"),
            Task(description="Identify key competitors", id="task_2", dependencies=["task_1"]),
            Task(description="Draft strategy report", id="task_3", dependencies=["task_2"]),
            Task(description="Review and finalize", id="task_4", dependencies=["task_3"])
        ]
        return tasks

class TaskGraph:
    def __init__(self, tasks: List[Task]):
        self.tasks = {t.id: t for t in tasks}

    def get_ready_tasks(self) -> List[Task]:
        ready = []
        for task in self.tasks.values():
            if task.status != "PENDING":
                continue
            
            # Check if all dependencies are completed
            deps_met = True
            for dep_id in task.dependencies:
                dep_task = self.tasks.get(dep_id)
                if not dep_task or dep_task.status != "COMPLETED":
                    deps_met = False
                    break
            
            if deps_met:
                ready.append(task)
        return ready

    def update_task_status(self, task_id: str, status: str, result: Any = None):
        if task_id in self.tasks:
            self.tasks[task_id].status = status
            self.tasks[task_id].result = result

    def is_complete(self) -> bool:
        return all(t.status == "COMPLETED" for t in self.tasks.values())
