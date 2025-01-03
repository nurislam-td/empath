from typing import Protocol
from uuid import UUID

from application.auth.ports.jwt import JWTPair
from domain.auth import entities


class AuthRepo(Protocol):
    async def create_user(self, user: entities.User) -> None: ...

    async def create_jwt(self, jwt: JWTPair, user_id: UUID) -> None: ...

    async def refresh_jwt(self, jwt: JWTPair, user_id: UUID) -> None: ...


class AuthReader(Protocol):
    async def get_user_by_email(self, email: str) -> entities.User: ...

    async def get_user_code_by_email(self, email: str) -> str: ...
