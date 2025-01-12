from typing import Any
from uuid import UUID

from sqlalchemy import insert, select, update

from application.auth.ports.jwt import JWTPair
from application.auth.ports.repo import AuthReader, AuthRepo
from domain.auth import entities
from infrastructure.auth.mapper import (
    convert_db_model_to_user_entity,
    convert_user_entity_to_db_model,
)
from infrastructure.auth.models import RefreshToken, User
from infrastructure.db.repositories.base import AlchemyReader, AlchemyRepo


class AlchemyAuthRepo(AlchemyRepo, AuthRepo):
    user = User
    refresh_token = RefreshToken

    async def create_user(self, user: entities.User) -> None:
        query = insert(self.user).values(**convert_user_entity_to_db_model(user=user))
        await self.execute(query=query)

    async def update_user(self, values: dict[str, Any], filters: dict[str, Any]):
        query = update(self.user).values(**values).filter_by(**filters)
        await self.execute(query=query)

    async def create_jwt(self, jwt: JWTPair, user_id: UUID) -> None:
        query = insert(self.refresh_token).values(
            **dict(refresh_token=jwt.refresh_token, user_id=user_id)
        )
        await self.execute(query=query)

    async def refresh_jwt(self, jwt: JWTPair, user_id: UUID) -> None:
        query = (
            update(self.refresh_token)
            .values(refresh_token=jwt.refresh_token)
            .where(self.refresh_token.user_id == user_id)
        )
        await self.execute(query=query)


class AlchemyAuthReader(AlchemyReader, AuthReader):
    user = User

    async def get_user_by_email(self, email: str) -> entities.User:
        if not (
            user_map := await self.fetch_one(
                select(self.user.__table__).where(self.user.email == email)
            )
        ):
            raise Exception(
                "User with that email not exists"
            )  # TODO custom Repo exception
        return convert_db_model_to_user_entity(user=user_map)
