import sqlite3
import os
from typing import Optional, List, Tuple, Any
from contextlib import contextmanager
import logging


class DatabaseManager:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), '..', 'secure_vault.db')
        self._setup_logging()

    def _setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    @contextmanager
    def get_connection(self):
        connection = None
        try:
            connection = sqlite3.connect(self.db_path, check_same_thread=False)
            connection.row_factory = sqlite3.Row
            yield connection
        except sqlite3.Error as e:
            self.logger.error(f"Database error: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            if connection:
                connection.close()

    def initialize_db(self) -> bool:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL UNIQUE,
                        password_hash BLOB NOT NULL,
                        salt BLOB NOT NULL,
                        master_key_salt BLOB NOT NULL,
                        encrypted_master_key BLOB NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS vault_entries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        service_name TEXT NOT NULL,
                        username TEXT NOT NULL,
                        encrypted_password BLOB NOT NULL,
                        encrypted_notes BLOB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    )
                """)

                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_users_username 
                    ON users(username)
                """)

                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_vault_entries_user_id 
                    ON vault_entries(user_id)
                """)

                conn.commit()
                return True
        except sqlite3.Error as e:
            self.logger.error(f"Database initialization error: {e}")
            return False

    def execute_query(self, query: str, params: Optional[Tuple] = None) -> bool:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params or ())
                conn.commit()
                return True
        except sqlite3.Error as e:
            self.logger.error(f"Query execution error: {e}")
            return False

    def fetch_one(self, query: str, params: Optional[Tuple] = None) -> Optional[Tuple]:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params or ())
                result = cursor.fetchone()
                return tuple(result) if result else None
        except sqlite3.Error as e:
            self.logger.error(f"Fetch one error: {e}")
            return None

    def fetch_all(self, query: str, params: Optional[Tuple] = None) -> List[Tuple]:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params or ())
                results = cursor.fetchall()
                return [tuple(row) for row in results]
        except sqlite3.Error as e:
            self.logger.error(f"Fetch all error: {e}")
            return []
