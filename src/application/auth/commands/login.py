from dataclasses import dataclass

from application.auth.ports.jwt import JWTManager
from application.auth.ports.pwd_manager import PasswordManager
from application.auth.ports.repo import AuthReader, AuthRepo
from application.common.command import Command, CommandHandler
from application.common.uow import UnitOfWork
from domain.auth.value_objects.jwt import JWTPair


@dataclass
class Login(Command[JWTPair]):
    email: str
    password: str


@dataclass
class LoginHandler(CommandHandler[Login, JWTPair]):
    uow: UnitOfWork
    auth_reader: AuthReader
    auth_repo: AuthRepo
    pwd_manager: PasswordManager
    jwt_manager: JWTManager

    async def __call__(self, command: Login) -> JWTPair:
        user = await self.auth_reader.get_user_by_email(email=command.email)
        if not self.pwd_manager.verify_password(
            password=command.password, hash_password=user.password
        ):
            raise Exception("invalid credentials")  # TODO InvalidCredentialsError
        jwt = self.jwt_manager.create_pair(
            payload=dict(sub=str(user.id), email=command.email)
        )
        await self.auth_repo.refresh_jwt(jwt=jwt, user_id=user.id)
        await self.uow.commit()
        return jwt
