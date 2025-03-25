from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from auth.application.ports.jwt import JWTManager


@dataclass(slots=True)
class PyJWTManager(JWTManager):
    def _encode_jwt(self, payload: dict[str, Any], expire_minutes: int, key: str) -> str:
        to_encode = payload.copy()
        now = datetime.now(tz=UTC)
        expire = now + timedelta(minutes=expire_minutes)
        to_encode.update(
            exp=expire,
            iat=now,
        )
        return jwt.encode(payload=to_encode, key=key, algorithm=self.jwt_alg)

    def _decode_jwt(self, token: str, key: str) -> dict[str, Any]:
        return jwt.decode(jwt=token, key=key, algorithms=[self.jwt_alg])
