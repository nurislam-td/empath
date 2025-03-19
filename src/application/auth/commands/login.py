from dataclasses import dataclass

from application.auth.exceptions import InvalidCredentialsError
from application.auth.ports.jwt import JWTManager
from application.auth.ports.pwd_manager import IPasswordManager
from application.auth.ports.repo import AuthRepo
from application.common.command import Command, CommandHandler
from application.common.uow import UnitOfWork
from application.users.ports.repo import UserReader
from domain.auth.value_objects.jwt import JWTPair
from domain.users.value_objects.email import Email
from domain.users.value_objects.password import Password


@dataclass(frozen=True)
class Login(Command[JWTPair]):
    email: str
    password: str


@dataclass(slots=True)
class LoginHandler(CommandHandler[Login, JWTPair]):
    uow: UnitOfWork
    auth_repo: AuthRepo
    user_reader: UserReader
    pwd_manager: IPasswordManager
    jwt_manager: JWTManager

    async def __call__(self, command: Login) -> JWTPair:
        user = await self.user_reader.get_user_by_email(email=Email(command.email).to_base())
        if not self.pwd_manager.verify_password(
            password=Password(command.password).to_base(), hash_password=user.password
        ):
            raise InvalidCredentialsError()
        jwt = self.jwt_manager.create_pair(payload=dict(sub=str(user.id), email=command.email))
        await self.auth_repo.refresh_jwt(jwt=jwt, user_id=user.id)
        await self.uow.commit()
        return jwt
