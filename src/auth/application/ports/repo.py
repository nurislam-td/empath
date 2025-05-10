from datetime import timedelta
from typing import Protocol
from uuid import UUID

from auth.application.ports.jwt import JWTPair


class AuthRepo(Protocol):
    async def create_jwt(self, jwt: JWTPair, user_id: UUID) -> None: ...

    async def refresh_jwt(self, jwt: JWTPair, user_id: UUID) -> None: ...

    async def delete_refresh_jwt(self, user_id: UUID) -> None: ...


class AuthReader(Protocol):
    async def get_refresh_token(self, user_id: UUID) -> str: ...


class VerifyCodeRepo(Protocol):
    async def set_verify_code(self, email: str, code: str, expires_in: int | timedelta | None = None) -> None: ...

    async def get_verify_code(self, email: str) -> str | None: ...
