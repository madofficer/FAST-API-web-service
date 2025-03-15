from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"])


class PasswordCheck:
    @staticmethod
    def generate_password_hash(password: str) -> str:
        hash_ = password_context.hash(password)
        return hash_

    @staticmethod
    def verify_password(password: str, hash_: str) -> bool:
        return password_context.verify(password, hash_)
