from uuid import UUID

from sqlalchemy import insert, select, update

from application.auth.ports.jwt import JWTPair
from application.auth.ports.repo import AuthReader, AuthRepo
from infrastructure.auth.models import RefreshToken
from infrastructure.db.repositories.base import AlchemyReader, AlchemyRepo


class AlchemyAuthRepo(AlchemyRepo, AuthRepo):
    refresh_token = RefreshToken

    async def create_jwt(self, jwt: JWTPair, user_id: UUID) -> None:
        query = insert(self.refresh_token).values(
            **dict(refresh_token=jwt.refresh_token, user_id=user_id)
        )
        await self.execute(query=query)

    async def refresh_jwt(self, jwt: JWTPair, user_id: UUID) -> None:
        query = (
            update(self.refresh_token)
            .values(refresh_token=jwt.refresh_token)
            .where(self.refresh_token.user_id == user_id)  # type: ignore
        )
        await self.execute(query=query)


class AlchemyAuthReader(AlchemyReader, AuthReader):
    token = RefreshToken

    async def get_refresh_token(self, user_id: UUID) -> str:
        refresh_token = await self.fetch_one(  # type: ignore
            select(self.token.__table__).where(self.token.user_id == user_id)  # type: ignore
        )
        if not refresh_token:
            raise Exception(
                "Token for user: {user_id} not found"
            )  # TODO custom exception
        return refresh_token.refresh_token
