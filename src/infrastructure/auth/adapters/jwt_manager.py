from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from application.auth.ports.jwt import JWTManager


@dataclass(slots=True)
class PyJWTManager(JWTManager):
    def _encode_jwt(
        self, payload: dict[str, Any], expire_minutes: int, key: str
    ) -> str:
        to_encode = payload.copy()
        now = datetime.now(tz=timezone.utc)
        expire = now + timedelta(minutes=expire_minutes)
        to_encode.update(
            exp=expire,
            iat=now,
        )
        encoded = jwt.encode(payload=to_encode, key=key, algorithm=self.jwt_alg)
        return encoded

    def _decode_jwt(self, token: str, key: str) -> dict[str, Any]:
        return jwt.decode(jwt=token, key=key, algorithms=[self.jwt_alg])
