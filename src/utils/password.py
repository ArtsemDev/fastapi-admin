from passlib.context import CryptContext

__all__ = [
    "PasswordContext",
]


class PasswordContext(object):
    context = CryptContext(schemes="bcrypt", deprecated="auto")

    @classmethod
    def hash(cls, password: str) -> str:
        return cls.context.hash(secret=password)

    @classmethod
    def verify(cls, password: str, password_hash: str) -> bool:
        return cls.context.verify(secret=password, hash=password_hash)
