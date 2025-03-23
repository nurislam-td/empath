from dataclasses import dataclass

from auth.application.ports.pwd_manager import IPasswordManager
from common.application.command import Command, CommandHandler
from common.application.uow import UnitOfWork
from users.application.ports.repo import UserReader, UserRepo
from users.domain.value_objects.email import Email
from users.domain.value_objects.password import Password


@dataclass(slots=True, frozen=True)
class ForgetPassword(Command[None]):
    email: str
    password: str


@dataclass(slots=True, frozen=True)
class ForgetPasswordHandler(CommandHandler[ForgetPassword, None]):
    _uow: UnitOfWork
    _user_repo: UserRepo
    _user_reader: UserReader
    _pwd_manager: IPasswordManager

    async def __call__(self, command: ForgetPassword) -> None:
        user = await self._user_reader.get_user_by_email(email=Email(command.email).to_base())
        await self._user_repo.update_user(
            values={"password": self._pwd_manager.hash_password(Password(command.password).to_base())},
            filters={"id": user.id},
        )
        await self._uow.commit()
