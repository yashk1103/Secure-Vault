from typing import Optional, Dict, Any
from database_manager_sqlite import DatabaseManager
from crypto_utils import CryptoUtils


class AuthManager:
    MIN_USERNAME_LENGTH = 3
    MIN_PASSWORD_LENGTH = 8

    def __init__(self, db_manager: DatabaseManager, crypto_utils: CryptoUtils):
        self.db_manager = db_manager
        self.crypto_utils = crypto_utils

    def register_user(self, username: str, password: str) -> bool:
        if not self._validate_credentials(username, password):
            return False

        if self._user_exists(username):
            return False

        password_hash, salt = self.crypto_utils.hash_password(password)
        master_key = self.crypto_utils.generate_key()
        master_key_salt = self.crypto_utils.generate_salt()
        password_derived_key = self.crypto_utils.derive_key_from_password(password, master_key_salt)
        encrypted_master_key = self.crypto_utils.encrypt_master_key(master_key, password_derived_key)

        return self.db_manager.execute_query(
            """INSERT INTO users (username, password_hash, salt, master_key_salt, encrypted_master_key)
               VALUES (?, ?, ?, ?, ?)""",
            (username, password_hash, salt, master_key_salt, encrypted_master_key)
        )

    def login_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        user_data = self.db_manager.fetch_one(
            """SELECT id, username, password_hash, salt, master_key_salt, encrypted_master_key
               FROM users WHERE username = ?""",
            (username,)
        )

        if not user_data:
            return None

        user_id, stored_username, password_hash, salt, master_key_salt, encrypted_master_key = user_data

        if not self.crypto_utils.verify_password(password, password_hash):
            return None

        try:
            password_derived_key = self.crypto_utils.derive_key_from_password(password, master_key_salt)
            master_key = self.crypto_utils.decrypt_master_key(encrypted_master_key, password_derived_key)
        except Exception:
            return None

        return {
            'user': {
                'id': user_id,
                'username': stored_username
            },
            'master_key': master_key
        }

    def _validate_credentials(self, username: str, password: str) -> bool:
        return (len(username) >= self.MIN_USERNAME_LENGTH and 
                len(password) >= self.MIN_PASSWORD_LENGTH)

    def _user_exists(self, username: str) -> bool:
        return self.db_manager.fetch_one(
            "SELECT id FROM users WHERE username = ?", (username,)
        ) is not None
