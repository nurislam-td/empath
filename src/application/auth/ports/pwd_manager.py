from typing import Protocol


class PasswordManager(Protocol):
    @staticmethod
    def hash_password(password: str) -> bytes: ...

    @staticmethod
    def verify_password(password: str, hash_password: bytes) -> bool: ...

    @staticmethod
    def get_random_num(length: int = 6) -> str: ...
