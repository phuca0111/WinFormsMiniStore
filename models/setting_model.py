import sqlite3
from typing import Optional

class SettingModel:
    def __init__(self, db_path: str, table_name: str = 'settings'):
        self.db_path = db_path
        self.table_name = table_name

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def get(self, key: str) -> Optional[str]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT value FROM {self.table_name} WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row[0] if row else None

    def set(self, key: str, value: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT OR REPLACE INTO {self.table_name} (key, value) VALUES (?, ?)", (key, value))
            conn.commit() 