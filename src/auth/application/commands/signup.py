from dataclasses import dataclass

from auth.application.ports.jwt import JWTManager
from auth.application.ports.pwd_manager import IPasswordManager
from auth.application.ports.repo import AuthRepo
from auth.domain.value_objects.jwt import JWTPair
from common.application.command import Command, CommandHandler
from common.application.uow import UnitOfWork
from users.application.exceptions import UserEmailAlreadyExistError
from users.application.ports.repo import UserReader, UserRepo
from users.domain.entities import User
from users.domain.value_objects.email import Email
from users.domain.value_objects.nickname import Nickname
from users.domain.value_objects.password import Password


@dataclass(slots=True, frozen=True)
class SignUp(Command[JWTPair]):
    email: str
    password: str
    nickname: str


@dataclass(slots=True)
class SignUpHandler(CommandHandler[SignUp, JWTPair]):
    _user_repo: UserRepo
    _user_reader: UserReader
    _auth_repo: AuthRepo
    _jwt_manager: JWTManager
    _uow: UnitOfWork
    _pwd_manager: IPasswordManager

    async def __call__(self, command: SignUp) -> JWTPair:
        if await self._user_reader.check_email_existence(command.email):
            raise UserEmailAlreadyExistError(command.email)
        user = User(
            email=Email(command.email),
            password=self._pwd_manager.hash_password(Password(command.password).to_base()),
            nickname=Nickname(command.nickname),
        )
        jwt = self._jwt_manager.create_pair(payload={"sub": str(user.id), "email": command.email})
        await self._user_repo.create_user(user=user)
        await self._auth_repo.create_jwt(jwt=jwt, user_id=user.id)
        await self._uow.commit()
        return jwt
