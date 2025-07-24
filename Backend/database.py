import sqlite3
import os
def get_connection():
    """Conecta ao banco de dados SQLite"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Database", "roupas.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return sqlite3.connect(db_path)
