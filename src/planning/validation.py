from typing import List, Dict, Any
from .decomposition import Task, TaskGraph

class PlanValidator:
    def validate(self, graph: TaskGraph) -> Dict[str, Any]:
        """
        Validates the plan for:
        1. Cycle detection
        2. Resource availability (mocked)
        3. Feasibility (mocked)
        """
        print("[Validator] Validating task graph...")
        
        # 1. Very simple cycle detection (limited for mock)
        if self._has_cycle(graph):
            return {"valid": False, "error": "Cyclic dependencies detected in plan"}

        # 2. Mock feasibility check
        return {"valid": True, "error": None}

    def _has_cycle(self, graph: TaskGraph) -> bool:
        # Simple DFS for cycle detection
        visited = set()
        path = set()

        def visit(task_id):
            if task_id in path: return True
            if task_id in visited: return False
            
            visited.add(task_id)
            path.add(task_id)
            
            task = graph.tasks.get(task_id)
            if task:
                for dep_id in task.dependencies:
                    if visit(dep_id): return True
            
            path.remove(task_id)
            return False

        for task_id in graph.tasks:
            if visit(task_id): return True
        return False

class Replanner:
    def suggest_fixes(self, failed_task: Task, context: Dict[str, Any]) -> List[Task]:
        print(f"[Replanner] Analyzing failure of task: {failed_task.description}")
        # Logic to suggest alternative tasks
        return []
