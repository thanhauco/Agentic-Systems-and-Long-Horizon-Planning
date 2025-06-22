import sqlite3
import json
import datetime
from typing import List, Dict, Any, Optional

class SemanticMemory:
    def __init__(self, db_path: str = "agent_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memory_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT,
                    tags TEXT,
                    embedding_mock TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def add_memory(self, content: str, tags: List[str] = None):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO memory_entries (content, tags) VALUES (?, ?)",
                (content, json.dumps(tags or []))
            )
        print(f"[Memory] Added new experience: {content[:50]}...")

    def retrieve_relevant(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Simulates semantic retrieval. 
        In a real system, this would use vector embeddings.
        Here we use simple keyword matching in content/tags.
        """
        print(f"[Memory] Searching for lessons related to: '{query}'")
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            # Simple keyword mock
            query_part = f"%{query}%"
            rows = conn.execute(
                "SELECT * FROM memory_entries WHERE content LIKE ? OR tags LIKE ? ORDER BY created_at DESC LIMIT ?",
                (query_part, query_part, limit)
            ).fetchall()
            
            return [dict(row) for row in rows]

class LessonLearned:
    """Helper to structure feedback for memory."""
    @staticmethod
    def format_failure(task: str, error: str, fix: str) -> str:
        return f"Task '{task}' failed with error '{error}'. Recommended fix: {fix}"
