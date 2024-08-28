from dataclasses import dataclass

from domain.auth import entities
from domain.auth.value_objects.email import Email
from domain.auth.value_objects.nickname import Nickname
from domain.auth.value_objects.password import Password

from application.auth.ports.jwt import JWTManager, JWTPair
from application.auth.ports.repo import AuthRepo
from application.common.command import Command, CommandHandler


@dataclass(slots=True, frozen=True)
class SignUp(Command):
    email: str
    password: str
    nickname: str


class SignUpHandler(CommandHandler[SignUp, JWTPair]):
    def __init__(
        self, auth_repo: AuthRepo, mediator, uow, jwt_manager: JWTManager
    ) -> None:
        self._auth_repo = auth_repo
        self._jwt_manager = jwt_manager
        self._mediator = mediator
        self._uow = uow

    async def __call__(self, command: SignUp) -> JWTPair:
        user = entities.User(
            password=Password(command.password),
            email=Email(command.email),
            nickname=Nickname(command.nickname),
        )
        jwt = self._jwt_manager.create(payload=dict(sub=user.id, email=command.email))
        await self._auth_repo.create_user(user=user)
        await self._auth_repo.create_jwt(jwt=jwt, user_id=user.id)
        return jwt
