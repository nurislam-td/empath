from dataclasses import dataclass
from datetime import date
from typing import Any
from uuid import UUID

from common.application.command import Command, CommandHandler
from common.application.uow import UnitOfWork
from users.application.ports.repo import UserReader, UserRepo
from users.domain.enums.gender import Gender
from users.domain.value_objects.nickname import Nickname


@dataclass(slots=True, frozen=True)
class UpdateFullname(Command[None]):
    user_id: UUID
    name: str
    lastname: str
    patronymic: str


class UpdateFullnameHandler(CommandHandler[UpdateFullname, None]):
    def __init__(self, user_repo: UserRepo, user_reader: UserReader, uow: UnitOfWork) -> None:
        self._user_repo = user_repo
        self._user_reader = user_reader
        self._uow = uow

    async def __call__(self, command: UpdateFullname) -> None:
        user = await self._user_reader.get_user_by_id(user_id=command.user_id)
        values: dict[str, Any] = {
            "name": command.name,
            "lastname": command.lastname,
            "patronymic": command.patronymic,
        }
        await self._user_repo.update_user(values=values, filters={"id": user.id})
        await self._uow.commit()
