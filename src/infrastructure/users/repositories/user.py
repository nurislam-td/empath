from typing import Any
from uuid import UUID

from sqlalchemy import Select, insert, select, update

from application.common.dto import PaginatedDTO
from application.users.dto.user import UserDTO
from application.users.exceptions import UserEmailNotExistError, UserIdNotExistError
from application.users.ports.repo import UserReader, UserRepo
from domain.users import entities
from infrastructure.auth.models import User
from infrastructure.db.repositories.base import AlchemyReader, AlchemyRepo
from infrastructure.db.repositories.paginators import AlchemyPaginator
from infrastructure.users.mapper import (
    convert_db_model_to_dto,
    convert_db_model_to_user_entity,
    convert_user_entity_to_db_model,
)


class AlchemyUserRepo(AlchemyRepo, UserRepo):
    user = User

    async def create_user(self, user: entities.User) -> None:
        query = insert(self.user).values(**convert_user_entity_to_db_model(user=user))
        await self.execute(query=query)

    async def update_user(self, values: dict[str, Any], filters: dict[str, Any]):
        query = update(self.user).values(**values).filter_by(**filters)
        await self.execute(query=query)


class AlchemyUserReader(AlchemyReader, UserReader):
    user = User
    paginator = AlchemyPaginator

    def _get_users_query(self, filters: dict[str, Any] | None = None):
        query = select(self.user.__table__)
        if filters:
            query = query.filter_by(**filters)
        return query

    async def count(self, query: Select[Any]) -> int:
        return len(await self.fetch_all(query))

    async def get_paginated_users(
        self, page: int, per_page: int, filters: dict[str, Any] | None = None
    ) -> PaginatedDTO[UserDTO]:
        query = self._get_users_query(filters)
        paginated_query = self.paginator.paginate(
            query=query, page=page, per_page=per_page
        )
        value_count = await self.count(query)
        page_count = self.paginator.get_page_count(value_count, per_page)
        users = await self.fetch_all(paginated_query)
        if users:
            return PaginatedDTO[UserDTO](
                count=page_count,
                page=page,
                results=[convert_db_model_to_dto(user) for user in users],
            )

        return PaginatedDTO[UserDTO](count=page_count, page=page)

    async def get_user_by_email(self, email: str) -> entities.User:
        if not (
            user_map := await self.fetch_one(  # type: ignore
                select(self.user.__table__).where(self.user.email == email)
            )
        ):
            raise UserEmailNotExistError(email=email)
        return convert_db_model_to_user_entity(user=user_map)

    async def get_user_by_id(self, user_id: UUID) -> entities.User:
        if not (
            user_map := await self.fetch_one(  # type: ignore
                select(self.user.__table__).where(self.user.id == user_id)  # type: ignore
            )
        ):
            raise UserIdNotExistError(user_id=user_id)
        return convert_db_model_to_user_entity(user=user_map)

    async def check_email_existence(self, email: str) -> bool:
        return bool(
            await self.fetch_one(
                select(self.user.__table__).where(self.user.email == email)
            )
        )
