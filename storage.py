import sqlite3
import sys
import os 
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from pathlib import Path
from tracker.models import UsageRecord

DB_PATH = Path("data/usage.db")
LOG_PATH = Path("logs/usage.jsonl")

class StorageManager:
    def __init__(self):
        DB_PATH.parent.mkdir(exist_ok=True)
        LOG_PATH.parent.mkdir(exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    model TEXT,
                    input_tokens INTEGER,
                    output_tokens INTEGER,
                    total_tokens INTEGER,
                    prompt_preview TEXT,
                    response_preview TEXT,
                    duration_ms REAL
                )
            """)

    def save(self, record: UsageRecord):
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                INSERT INTO usage
                (timestamp, model, input_tokens, output_tokens,
                 total_tokens, prompt_preview, response_preview, duration_ms)
                VALUES (?,?,?,?,?,?,?,?)
            """, (
                record.timestamp, record.model,
                record.input_tokens, record.output_tokens,
                record.total_tokens, record.prompt_preview,
                record.response_preview, record.duration_ms
            ))
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(record.to_json() + "\n")
