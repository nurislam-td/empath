from dataclasses import asdict, dataclass
from uuid import UUID

from application.common.command import Command, CommandHandler
from application.common.uow import UnitOfWork
from application.users.ports.repo import UserReader, UserRepo
from domain.users.value_objects.password import Password


@dataclass(slots=True)
class UpdateUser(Command[None]):
    id: UUID
    name: str | None = None
    password: str | None = None


class UpdateUserHandler(CommandHandler[UpdateUser, None]):
    def __init__(self, user_repo: UserRepo, user_reader: UserReader, uow: UnitOfWork):
        self._user_repo = user_repo
        self._user_reader = user_reader
        self._uow = uow

    async def __call__(self, command: UpdateUser):
        user = await self._user_reader.get_user_by_id(user_id=command.id)
        if command.password:
            command.password = Password(command.password).to_base()

        await self._user_repo.update_user(
            values=asdict(command), filters=dict(id=user.id)
        )
        await self._uow.commit()
