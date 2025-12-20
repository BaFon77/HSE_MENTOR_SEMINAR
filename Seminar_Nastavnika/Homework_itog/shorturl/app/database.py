import os
import sqlite3
from pathlib import Path
from contextlib import contextmanager

DATA_DIR = Path(os.getenv("DATA_DIR", "/app/data"))
DB_PATH = Path(os.getenv("DB_PATH", str(DATA_DIR / "shorturl.db")))

@contextmanager
def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_id TEXT UNIQUE NOT NULL,
                full_url TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
                visits INTEGER NOT NULL DEFAULT 0
        )
    """)
     