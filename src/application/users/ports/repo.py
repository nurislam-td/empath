from typing import Any, Protocol
from uuid import UUID

from domain.users import entities


class UserRepo(Protocol):
    async def create_user(self, user: entities.User) -> None: ...

    async def update_user(self, values: dict[str, Any], filters: dict[str, Any]): ...


class UserReader(Protocol):
    async def get_user_by_email(self, email: str) -> entities.User: ...

    async def get_user_by_id(self, user_id: UUID) -> entities.User: ...
