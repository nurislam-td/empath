from dataclasses import dataclass

from application.auth.ports.jwt import JWTManager
from application.auth.ports.pwd_manager import PasswordManager
from application.auth.ports.repo import AuthRepo
from application.common.command import Command, CommandHandler
from application.common.uow import UnitOfWork
from domain.auth import entities
from domain.auth.value_objects.email import Email
from domain.auth.value_objects.jwt import JWTPair
from domain.auth.value_objects.nickname import Nickname
from domain.auth.value_objects.password import Password


@dataclass(slots=True, frozen=True)
class SignUp(Command):
    email: str
    password: str
    nickname: str


class SignUpHandler(CommandHandler[SignUp, JWTPair]):
    def __init__(
        self,
        auth_repo: AuthRepo,
        uow: UnitOfWork,
        jwt_manager: JWTManager,
        pwd_manager: PasswordManager,
    ) -> None:
        self._auth_repo = auth_repo
        self._jwt_manager = jwt_manager
        self._uow = uow
        self._pwd_manager = pwd_manager

    async def __call__(self, command: SignUp) -> JWTPair:
        user = entities.User(
            email=Email(command.email),
            password=self._pwd_manager.hash_password(
                Password(command.password).to_base()
            ),
            nickname=Nickname(command.nickname),
        )
        jwt = self._jwt_manager.create(
            payload=dict(sub=str(user.id), email=command.email)
        )
        await self._auth_repo.create_user(user=user)
        await self._auth_repo.create_jwt(jwt=jwt, user_id=user.id)
        await self._uow.commit()
        return jwt
