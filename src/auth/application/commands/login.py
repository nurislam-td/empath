from dataclasses import dataclass

from auth.application.exceptions import InvalidCredentialsError
from auth.application.ports.jwt import JWTManager
from auth.application.ports.pwd_manager import IPasswordManager
from auth.application.ports.repo import AuthRepo
from auth.domain.value_objects.jwt import JWTPair
from common.application.command import Command, CommandHandler
from common.application.uow import UnitOfWork
from users.application.ports.repo import UserReader
from users.domain.value_objects.email import Email
from users.domain.value_objects.password import Password


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
            password=Password(command.password).to_base(),
            hash_password=user.password,
        ):
            raise InvalidCredentialsError()
        jwt = self.jwt_manager.create_pair(payload={"sub": str(user.id), "email": command.email})
        await self.auth_repo.refresh_jwt(jwt=jwt, user_id=user.id)
        await self.uow.commit()
        return jwt
