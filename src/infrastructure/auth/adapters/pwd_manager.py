import random
import string

import bcrypt

from application.auth.ports import pwd_manager

NUM = string.digits


class PasswordManager(pwd_manager.IPasswordManager):
    @staticmethod
    def hash_password(password: str) -> bytes:
        salt = bcrypt.gensalt()
        password_b: bytes = password.encode()
        return bcrypt.hashpw(password_b, salt)

    @staticmethod
    def verify_password(password: str, hash_password: bytes) -> bool:
        return bcrypt.checkpw(password=password.encode(), hashed_password=hash_password)

    @staticmethod
    def get_random_num(length: int = 6) -> str:
        return "".join(random.choices(NUM, k=length))
