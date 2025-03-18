from datetime import timedelta, datetime
from jwt import PyJWTError
from passlib.context import CryptContext
from uuid import uuid4
from source.config import Config
import jwt
import logging

# todo change passlib to bcrypt
password_context = CryptContext(schemes=["bcrypt"])

ACCESS_TOKEN_EXPIRY = 3600


class PasswordCheck:
    @staticmethod
    def generate_password_hash(password: str) -> str:
        hash_ = password_context.hash(password)
        return hash_

    @staticmethod
    def verify_password(password: str, hash_: str) -> bool:
        return password_context.verify(password, hash_)


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):
    payload = {
        "user": user_data,
        "exp": datetime.now()
        + (expiry if expiry else timedelta(seconds=ACCESS_TOKEN_EXPIRY)),
        "jti": str(uuid4()),
        "refresh": refresh,
    }

    token = jwt.encode(
        payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except PyJWTError as err:
        logging.exception(err)
        return None
