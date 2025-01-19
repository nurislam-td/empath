from dataclasses import asdict, dataclass
from uuid import UUID

from application.auth.ports.repo import AuthReader, AuthRepo
from application.common.command import Command, CommandHandler
from application.common.uow import UnitOfWork
from domain.auth.value_objects.password import Password


@dataclass(slots=True)
class UpdateUser(Command[None]):
    id: UUID
    name: str | None = None
    password: str | None = None


class UpdateUserHandler(CommandHandler[UpdateUser, None]):
    def __init__(self, auth_repo: AuthRepo, auth_reader: AuthReader, uow: UnitOfWork):
        self._auth_repo = auth_repo
        self._auth_reader = auth_reader
        self._uow = uow

    async def __call__(self, command: UpdateUser):
        user = await self._auth_reader.get_user_by_id(user_id=command.id)
        if command.password:
            command.password = Password(command.password).to_base()

        await self._auth_repo.update_user(
            values=asdict(command), filters=dict(id=user.id)
        )
        await self._uow.commit()
