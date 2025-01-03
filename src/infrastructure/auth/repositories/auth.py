from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from application.auth.ports.jwt import JWTPair
from application.auth.ports.repo import AuthReader, AuthRepo
from domain.auth import entities
from infrastructure.auth.mapper import (
    convert_db_model_to_user_entity,
    convert_user_entity_to_db_model,
)
from infrastructure.auth.models import RefreshToken, User, VerifyCode
from infrastructure.db.repositories.base import AlchemyReader, AlchemyRepo


class AlchemyAuthRepo(AlchemyRepo, AuthRepo):
    user = User
    verify_code = VerifyCode
    refresh_token = RefreshToken

    async def create_user(self, user: entities.User) -> None:
        query = insert(self.user).values(**convert_user_entity_to_db_model(user=user))
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

    def __init__(self, session: AsyncSession, verify_code_store) -> None:
        super().__init__(session)
        self._verify_code_store = verify_code_store

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
