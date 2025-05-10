from typing import TYPE_CHECKING, Any, ClassVar
from uuid import UUID

from common.application.dto import PaginatedDTO
from users.application.dto.user import UserDTO
from users.application.exceptions import UserEmailNotExistError, UserIdNotExistError
from users.application.ports.repo import UserReader, UserRepo
from users.domain import entities
from users.domain.value_objects.email import Email
from users.domain.value_objects.nickname import Nickname
from users.infrastructure.mapper import convert_user_entity_to_user_dto

if TYPE_CHECKING:
    from collections.abc import Callable


class MockUserRepo(UserRepo, UserReader):
    users: ClassVar[dict[UUID, entities.User]] = {}

    async def create_user(self, user: entities.User) -> None:
        self.users[user.id] = user

    async def update_user(self, values: dict[str, Any], filters: dict[str, Any]) -> None:
        convert_strategy: dict[str, Callable[[Any], Any]] = {
            "email": lambda x: Email(x),
            "nickname": lambda x: Nickname(x),
        }
        user = self.users[filters["id"]]
        for key, value in values.items():
            setattr(user, key, convert_strategy.get(key, lambda x: x)(value))
        self.users[filters["id"]] = user

    async def get_user_by_email(self, email: str) -> entities.User:
        user = next(x for x in self.users.values() if x.email.value == email)
        if not user:
            raise UserEmailNotExistError(email=email)
        return user

    async def get_user_by_id(self, user_id: UUID) -> entities.User:
        user = self.users.get(user_id)
        if not user:
            raise UserIdNotExistError(user_id=user_id)
        return user

    async def get_paginated_users(
        self,
        page: int,
        per_page: int,
        filters: dict[str, Any] | None = None,
    ) -> PaginatedDTO[UserDTO]:
        users = [convert_user_entity_to_user_dto(user) for user in self.users.values()]

        if filters:
            users = [user for user in users if all(getattr(user, k) == v for k, v in filters.items())]
        count = len(users)
        users = users[(page - 1) * per_page : page * per_page]
        return PaginatedDTO[UserDTO](
            count=count,
            page=page,
            results=users,
        )

    async def check_email_existence(self, email: str) -> bool:
        return any(user.email.value == email for user in self.users.values())
