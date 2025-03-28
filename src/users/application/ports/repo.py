from typing import Any, Protocol
from uuid import UUID

from common.application.dto import PaginatedDTO
from users.application.dto.user import UserDTO
from users.domain import entities


class UserRepo(Protocol):
    async def create_user(self, user: entities.User) -> None: ...

    async def update_user(self, values: dict[str, Any], filters: dict[str, Any]) -> None: ...


class UserReader(Protocol):
    async def get_user_by_email(self, email: str) -> entities.User: ...

    async def get_user_by_id(self, user_id: UUID) -> entities.User: ...

    async def get_paginated_users(
        self,
        page: int,
        per_page: int,
        filters: dict[str, Any] | None = None,
    ) -> PaginatedDTO[UserDTO]: ...

    async def check_email_existence(self, email: str) -> bool: ...
