from typing import Any
from uuid import UUID

from sqlalchemy import insert, select, update

from application.users.ports.repo import UserReader, UserRepo
from domain.users import entities
from infrastructure.auth.models import User
from infrastructure.db.repositories.base import AlchemyReader, AlchemyRepo
from infrastructure.users.mapper import (
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

    async def get_user_by_email(self, email: str) -> entities.User:
        if not (
            user_map := await self.fetch_one(  # type: ignore
                select(self.user.__table__).where(self.user.email == email)
            )
        ):
            raise Exception(
                "User with that email not exists"
            )  # TODO custom Repo exception
        return convert_db_model_to_user_entity(user=user_map)

    async def get_user_by_id(self, user_id: UUID) -> entities.User:
        if not (
            user_map := await self.fetch_one(  # type: ignore
                select(self.user.__table__).where(self.user.id == user_id)  # type: ignore
            )
        ):
            raise Exception(
                "User with that email not exists"
            )  # TODO custom Repo exception
        return convert_db_model_to_user_entity(user=user_map)
