from typing import Protocol

from domain.auth import entities

from application.auth.ports.jwt import JWTPair


class AuthRepo(Protocol):
    async def create_user(self, user: entities.User) -> None: ...

    async def save_jwt(self, jwt: JWTPair) -> None: ...
