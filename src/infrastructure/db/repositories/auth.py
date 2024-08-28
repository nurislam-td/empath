from uuid import UUID

from sqlalchemy import insert

from src.application.auth.ports.jwt import JWTPair
from src.application.auth.ports.repo import AuthRepo
from src.domain.auth import entities
from src.infrastructure.db.models.auth import RefreshToken, User, VerifyCode
from src.infrastructure.db.repositories.base import AlchemyRepo


class AlchemyAuthRepo(AuthRepo, AlchemyRepo):
    user = User
    verify_code = VerifyCode
    refresh_token = RefreshToken

    async def create_user(self, user: entities.User) -> None:
        query = insert(self.user).values(user.to_dict())
        await self.execute(query)

    async def create_jwt(self, jwt: JWTPair, user_id: UUID) -> None:
        query = insert(self.refresh_token).values(
            dict(refresh_token=jwt.refresh_token, user_id=user_id)
        )
        await self.execute(query=query)
