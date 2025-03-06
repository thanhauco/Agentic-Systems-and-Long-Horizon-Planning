import sqlite3
import json
import os
from typing import Optional
from .agent import AgentState

class StateStore:
    def __init__(self, db_path: str = "agent_state.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS states (
                    agent_id TEXT PRIMARY KEY,
                    data TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def save_state(self, state: AgentState):
        data = json.dumps(state.to_dict())
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO states (agent_id, data, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)",
                (state.agent_id, data)
            )

    def load_state(self, agent_id: str) -> Optional[AgentState]:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT data FROM states WHERE agent_id = ?", (agent_id,)).fetchone()
            if row:
                return AgentState.from_dict(json.loads(row[0]))
        return None

    def list_agents(self):
        with sqlite3.connect(self.db_path) as conn:
            return [row[0] for row in conn.execute("SELECT agent_id FROM states").fetchall()]
