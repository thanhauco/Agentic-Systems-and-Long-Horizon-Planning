import json
from dataclasses import asdict
from typing import Dict, List, Any
from .decomposition import TaskGraph

class CheckpointManager:
    def __init__(self):
        self.history: List[Dict[str, Any]] = []

    def create_checkpoint(self, graph: TaskGraph, metadata: Dict[str, Any] = None):
        """Creates a snapshot of the current plan state."""
        checkpoint = {
            "step": len(self.history),
            "state": {tid: asdict(t) for tid, t in graph.tasks.items()},
            "metadata": metadata or {}
        }
        self.history.append(checkpoint)
        print(f"[Checkpoint] Created checkpoint {checkpoint['step']}")
        return checkpoint['step']

    def rollback(self, checkpoint_id: int) -> Dict[str, Any]:
        """Returns the state at a given checkpoint."""
        if 0 <= checkpoint_id < len(self.history):
            print(f"[Checkpoint] Rolling back to checkpoint {checkpoint_id}")
            return self.history[checkpoint_id]["state"]
        raise ValueError("Invalid checkpoint ID")

    def get_latest(self) -> Optional[Dict[str, Any]]:
        return self.history[-1] if self.history else None
