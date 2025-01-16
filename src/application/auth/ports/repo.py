from datetime import timedelta
from typing import Any, Protocol
from uuid import UUID

from application.auth.ports.jwt import JWTPair
from domain.auth import entities


class AuthRepo(Protocol):
    async def create_user(self, user: entities.User) -> None: ...

    async def update_user(self, values: dict[str, Any], filters: dict[str, Any]): ...

    async def create_jwt(self, jwt: JWTPair, user_id: UUID) -> None: ...

    async def refresh_jwt(self, jwt: JWTPair, user_id: UUID) -> None: ...


class AuthReader(Protocol):
    async def get_user_by_email(self, email: str) -> entities.User: ...

    async def get_user_code_by_email(self, email: str) -> str: ...

    async def get_user_by_id(self, user_id: UUID) -> entities.User: ...


class VerifyCodeRepo(Protocol):
    async def set_verify_code(
        self, email: str, code: str, expires_in: int | timedelta | None = None
    ): ...

    async def get_verify_code(self, email: str) -> str | None: ...
