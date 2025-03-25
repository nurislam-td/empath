from dataclasses import dataclass
from uuid import UUID

from auth.application.exceptions import InvalidPreviousPasswordError
from auth.application.ports.pwd_manager import IPasswordManager
from common.application.command import Command, CommandHandler
from common.application.uow import UnitOfWork
from users.application.ports.repo import UserReader, UserRepo
from users.domain.value_objects.password import Password


@dataclass(slots=True, frozen=True)
class ResetPassword(Command[None]):
    old_password: str
    new_password: str
    user_id: UUID


class ResetPasswordHandler(CommandHandler[ResetPassword, None]):
    def __init__(
        self,
        user_repo: UserRepo,
        user_reader: UserReader,
        uow: UnitOfWork,
        pwd_manager: IPasswordManager,
    ) -> None:
        self._user_repo = user_repo
        self._user_reader = user_reader
        self._uow = uow
        self._pwd_manager = pwd_manager

    async def __call__(self, command: ResetPassword) -> None:
        user = await self._user_reader.get_user_by_id(command.user_id)
        if self._pwd_manager.verify_password(command.old_password, hash_password=user.password):
            await self._user_repo.update_user(
                values={"password": self._pwd_manager.hash_password(Password(command.new_password).to_base())},
                filters={"id": command.user_id},
            )
            await self._uow.commit()
            return

        raise InvalidPreviousPasswordError
