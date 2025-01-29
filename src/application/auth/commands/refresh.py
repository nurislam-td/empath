from dataclasses import dataclass

from application.auth.exceptions import InvalidRefreshTokenError
from application.auth.ports.jwt import JWTManager
from application.auth.ports.repo import AuthReader, AuthRepo
from application.common.command import Command, CommandHandler
from application.common.uow import UnitOfWork
from domain.auth.value_objects.jwt import JWTPair


@dataclass
class Refresh(Command[JWTPair]):
    refresh_token: str


class RefreshHandler(CommandHandler[Refresh, JWTPair]):
    def __init__(
        self,
        jwt_manager: JWTManager,
        auth_repo: AuthRepo,
        auth_reader: AuthReader,
        uow: UnitOfWork,
    ):
        self._jwt_manager = jwt_manager
        self._auth_repo = auth_repo
        self._auth_reader = auth_reader
        self._uow = uow

    async def __call__(self, command: Refresh) -> JWTPair:
        payload = self._jwt_manager.decode_refresh(refresh_token=command.refresh_token)
        refresh_token = await self._auth_reader.get_refresh_token(
            user_id=payload["sub"]
        )
        if refresh_token != command.refresh_token:
            raise InvalidRefreshTokenError()
        jwt_pair = self._jwt_manager.create_pair(payload=payload)
        await self._auth_repo.refresh_jwt(jwt=jwt_pair, user_id=payload["sub"])
        await self._uow.commit()
        return jwt_pair
