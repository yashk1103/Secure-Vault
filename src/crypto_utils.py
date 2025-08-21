import os
import bcrypt
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from typing import Tuple


class CryptoUtils:
    PBKDF2_ITERATIONS = 100000
    SALT_LENGTH = 32

    def hash_password(self, password: str) -> Tuple[bytes, bytes]:
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        return password_hash, salt

    def verify_password(self, password: str, password_hash: bytes) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), password_hash)

    def generate_key(self) -> bytes:
        return Fernet.generate_key()

    def generate_salt(self) -> bytes:
        return os.urandom(self.SALT_LENGTH)

    def derive_key_from_password(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.PBKDF2_ITERATIONS,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))

    def encrypt_data(self, data: str, key: bytes) -> bytes:
        if isinstance(data, str):
            data = data.encode('utf-8')
        return Fernet(key).encrypt(data)

    def decrypt_data(self, encrypted_data: bytes, key: bytes) -> str:
        return Fernet(key).decrypt(encrypted_data).decode('utf-8')

    def encrypt_master_key(self, master_key: bytes, password_derived_key: bytes) -> bytes:
        return Fernet(password_derived_key).encrypt(master_key)

    def decrypt_master_key(self, encrypted_master_key: bytes, password_derived_key: bytes) -> bytes:
        return Fernet(password_derived_key).decrypt(encrypted_master_key)
