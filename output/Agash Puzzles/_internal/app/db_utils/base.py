import sqlite3
from pathlib import Path


class DatabaseConnection:
    """Контекстный менеджер для подключения к SQLite."""
    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.commit()
            self.connection.close()


def execute_query(db_path, query, params=()):
    """Выполняет запрос и возвращает результат."""
    with DatabaseConnection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()


def execute_action(db_path, query, params=()):
    """Выполняет действие (INSERT, UPDATE, DELETE)."""
    with DatabaseConnection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
