from dataclasses import dataclass

from application.auth.ports.pwd_manager import IPasswordManager
from application.auth.ports.repo import AuthReader, AuthRepo
from application.common.command import Command, CommandHandler
from application.common.uow import UnitOfWork
from domain.auth.value_objects.password import Password


@dataclass(slots=True)
class ForgetPassword(Command):
    email: str
    password: str


@dataclass(slots=True, frozen=True)
class ForgetPasswordHandler(CommandHandler[ForgetPassword, None]):
    _uow: UnitOfWork
    _auth_repo: AuthRepo
    _auth_reader: AuthReader
    _pwd_manager: IPasswordManager

    async def __call__(self, command: ForgetPassword) -> None:
        user = await self._auth_reader.get_user_by_email(email=command.email)
        await self._auth_repo.update_user(
            values=dict(
                password=self._pwd_manager.hash_password(
                    Password(command.password).to_base()
                )
            ),
            filters=dict(id=user.id),
        )
        await self._uow.commit()
