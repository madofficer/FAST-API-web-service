from dataclasses import dataclass
from datetime import datetime
import hashlib


@dataclass
class User:
    """
    User Entity
    """

    username: str
    password_hash: str
    token_: str | None
    created_at: datetime = datetime.now()


    @staticmethod
    def hash_password(password: str, salt) -> str:
        return hashlib.sha256((password + salt).encode()).hexdigest()
