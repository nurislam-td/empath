from dataclasses import dataclass

from application.auth.ports.jwt import JWTManager
from application.common.command import Command, CommandHandler
from domain.auth.value_objects.jwt import JWTPair


@dataclass
class Refresh(Command[JWTPair]):
    refresh_token: str


class RefreshHandler(CommandHandler[Refresh, JWTPair]):
    def __init__(self, jwt_manager: JWTManager):
        self._jwt_manager = jwt_manager

    async def __call__(self, command: Refresh) -> JWTPair:
        payload = self._jwt_manager.decode_refresh(refresh_token=command.refresh_token)
        return self._jwt_manager.create_pair(payload=payload)
