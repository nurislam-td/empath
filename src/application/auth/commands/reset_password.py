from dataclasses import dataclass
from uuid import UUID

from application.auth.ports.repo import AuthReader, AuthRepo
from application.common.command import Command, CommandHandler
from application.common.uow import UnitOfWork
from infrastructure.auth.adapters.pwd_manager import PasswordManager


@dataclass(slots=True)
class ResetPassword(Command):
    old_password: str
    new_password: str
    user_id: UUID


class ResetPasswordHandler(CommandHandler[ResetPassword, None]):
    def __init__(
        self,
        auth_repo: AuthRepo,
        auth_reader: AuthReader,
        uow: UnitOfWork,
        pwd_manager: PasswordManager,
    ) -> None:
        self._auth_repo = auth_repo
        self._auth_reader = auth_reader
        self._uow = uow
        self._pwd_manager = pwd_manager

    async def __call__(self, command: ResetPassword) -> None:
        user = await self._auth_reader.get_user_by_id(command.user_id)
        if self._pwd_manager.verify_password(
            command.old_password, hash_password=user.password
        ):
            await self._auth_repo.update_user(
                values=dict(password=command.new_password),
                filters=dict(id=command.user_id),
            )
            await self._uow.commit()

        raise Exception("Incorrect prev pass")  # TODO custom exception
