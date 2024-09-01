from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, NamedTuple


class JWTPair(NamedTuple):
    access_token: str
    refresh_token: str


@dataclass(slots=True)
class JWTManager(ABC):
    jwt_alg: str
    access_private_path: Path
    access_public_path: Path
    access_token_expire: int
    refresh_private_path: Path
    refresh_public_path: Path
    refresh_token_expire: int

    @staticmethod
    @abstractmethod
    def encode_jwt(
        payload: dict[str, Any], expire_minutes: int, key: str, algorithm: str
    ) -> str: ...

    def create(self, payload: dict[str, Any]) -> JWTPair:
        access_token = self.encode_jwt(
            payload=payload,
            expire_minutes=self.access_token_expire,
            key=self.access_private_path.read_text(),
            algorithm=self.jwt_alg,
        )
        refresh_token = self.encode_jwt(
            payload=payload,
            expire_minutes=self.refresh_token_expire,
            key=self.refresh_private_path.read_text(),
            algorithm=self.jwt_alg,
        )
        return JWTPair(access_token, refresh_token)
