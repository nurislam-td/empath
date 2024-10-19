from typing import Protocol
from uuid import UUID

from domain.auth import entities

from application.auth.ports.jwt import JWTPair


class AuthRepo(Protocol):
    async def create_user(self, user: entities.User) -> None: ...

    async def create_jwt(self, jwt: JWTPair, user_id: UUID) -> None: ...

    async def refresh_jwt(self, jwt: JWTPair, user_id: UUID) -> None: ...


class AuthReader(Protocol):
    async def get_user_by_email(self, email: str) -> entities.User: ...
