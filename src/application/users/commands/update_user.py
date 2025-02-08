from dataclasses import asdict, dataclass
from datetime import date
from uuid import UUID

from application.common.command import Command, CommandHandler
from application.common.uow import UnitOfWork
from application.users.ports.repo import UserReader, UserRepo
from domain.users.enums.gender import Gender
from domain.users.value_objects.nickname import Nickname


@dataclass(slots=True)
class UpdateUser(Command[None]):
    user_id: UUID
    nickname: str
    gender: Gender
    name: str | None = None
    lastname: str | None = None
    patronymic: str | None = None
    date_birth: date | None = None


class UpdateUserHandler(CommandHandler[UpdateUser, None]):
    def __init__(self, user_repo: UserRepo, user_reader: UserReader, uow: UnitOfWork):
        self._user_repo = user_repo
        self._user_reader = user_reader
        self._uow = uow

    async def __call__(self, command: UpdateUser):
        user = await self._user_reader.get_user_by_id(user_id=command.user_id)
        values = dict(
            nickname=Nickname(command.nickname).to_base(),
            gender=command.gender,
            name=command.name,
            lastname=command.lastname,
            patronymic=command.patronymic,
            date_birth=command.date_birth,
        )
        await self._user_repo.update_user(values=values, filters=dict(id=user.id))
        await self._uow.commit()
