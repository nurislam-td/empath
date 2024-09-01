from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from src.application.auth.ports.jwt import JWTManager


@dataclass(slots=True)
class PyJWTManager(JWTManager):
    @staticmethod
    def encode_jwt(
        payload: dict[str, Any], expire_minutes: int, key: str, algorithm: str
    ) -> str:
        to_encode = payload.copy()
        now = datetime.now(tz=timezone.utc)
        expire = now + timedelta(minutes=expire_minutes)
        to_encode.update(
            exp=expire,
            iat=now,
        )
        encoded = jwt.encode(payload=to_encode, key=key, algorithm=algorithm)
        return encoded
