from dataclasses import dataclass
from uuid import UUID

from auth.application.ports.repo import AuthRepo
from common.application.command import Command, CommandHandler
from common.application.uow import UnitOfWork


@dataclass(frozen=True, slots=True)
class Logout(Command[None]):
    user_id: UUID


@dataclass(frozen=True, slots=True)
class LogoutHandler(CommandHandler[Logout, None]):
    _auth_repo: AuthRepo
    _uow: UnitOfWork

    async def __call__(self, command: Logout) -> None:
        await self._auth_repo.delete_refresh_jwt(user_id=command.user_id)
        await self._uow.commit()
