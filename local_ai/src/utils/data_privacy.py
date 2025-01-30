from cryptography.fernet import Fernet
from pathlib import Path
import json

class DataEncryptor:
    def __init__(self):
        self.key_path = Path("data/secret.key")
        self.key = self._load_or_create_key()
        self.cipher = Fernet(self.key)

    def _load_or_create_key(self) -> bytes:
        if not self.key_path.exists():
            self.key_path.parent.mkdir(parents=True, exist_ok=True)
            key = Fernet.generate_key()
            self.key_path.write_bytes(key)
            self.key_path.chmod(0o600)  # Secure permissions
            return key
        return self.key_path.read_bytes()

    def encrypt_data(self, data: str) -> bytes:
        """Encrypt sensitive data"""
        return self.cipher.encrypt(data.encode())

    def decrypt_data(self, encrypted_data: bytes) -> str:
        """Decrypt protected data"""
        return self.cipher.decrypt(encrypted_data).decode()

    def save_encrypted_history(self, history: list, file_path: Path):
        """Save conversation history securely"""
        encrypted = self.encrypt_data(json.dumps(history))
        file_path.write_bytes(encrypted)

    def load_encrypted_history(self, file_path: Path) -> list:
        """Load encrypted conversation history"""
        encrypted_data = file_path.read_bytes()
        return json.loads(self.decrypt_data(encrypted_data))