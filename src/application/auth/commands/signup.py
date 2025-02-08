from dataclasses import dataclass

from application.auth.ports.jwt import JWTManager
from application.auth.ports.pwd_manager import IPasswordManager
from application.auth.ports.repo import AuthRepo
from application.common.command import Command, CommandHandler
from application.common.uow import UnitOfWork
from application.users.ports.repo import UserRepo
from domain.auth.value_objects.jwt import JWTPair
from domain.users.entities import User
from domain.users.value_objects.email import Email
from domain.users.value_objects.nickname import Nickname
from domain.users.value_objects.password import Password


@dataclass(slots=True, frozen=True)
class SignUp(Command[JWTPair]):
    email: str
    password: str
    nickname: str


class SignUpHandler(CommandHandler[SignUp, JWTPair]):
    def __init__(
        self,
        user_repo: UserRepo,
        uow: UnitOfWork,
        jwt_manager: JWTManager,
        pwd_manager: IPasswordManager,
        auth_repo: AuthRepo,
    ) -> None:
        self._user_repo = user_repo
        self._auth_repo = auth_repo
        self._jwt_manager = jwt_manager
        self._uow = uow
        self._pwd_manager = pwd_manager

    async def __call__(self, command: SignUp) -> JWTPair:
        user = User(
            email=Email(command.email),
            password=self._pwd_manager.hash_password(
                Password(command.password).to_base()
            ),
            nickname=Nickname(command.nickname),
        )
        jwt = self._jwt_manager.create_pair(
            payload=dict(sub=str(user.id), email=command.email)
        )
        await self._user_repo.create_user(user=user)
        await self._auth_repo.create_jwt(jwt=jwt, user_id=user.id)
        await self._uow.commit()
        return jwt
