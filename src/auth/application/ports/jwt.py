from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from auth.domain.value_objects.jwt import JWTPair


@dataclass(slots=True)
class JWTManager(ABC):
    jwt_alg: str
    access_private_path: Path
    access_public_path: Path
    access_token_expire: int
    refresh_private_path: Path
    refresh_public_path: Path
    refresh_token_expire: int

    @abstractmethod
    def _encode_jwt(self, payload: dict[str, Any], expire_minutes: int, key: str) -> str: ...

    @abstractmethod
    def _decode_jwt(self, token: str, key: str) -> dict[str, Any]: ...

    def create_pair(self, payload: dict[str, Any]) -> JWTPair:
        access_token = self._encode_jwt(
            payload=payload,
            expire_minutes=self.access_token_expire,
            key=self.access_private_path.read_text(),
        )
        refresh_token = self._encode_jwt(
            payload=payload,
            expire_minutes=self.refresh_token_expire,
            key=self.refresh_private_path.read_text(),
        )
        return JWTPair(access_token, refresh_token)

    def decode_refresh(self, refresh_token: str) -> dict[str, Any]:
        return self._decode_jwt(token=refresh_token, key=self.refresh_public_path.read_text())

    def decode_access(self, access_token: str) -> dict[str, Any]:
        return self._decode_jwt(token=access_token, key=self.access_public_path.read_text())
