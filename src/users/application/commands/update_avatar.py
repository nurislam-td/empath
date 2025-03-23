from dataclasses import dataclass
from io import BytesIO
from uuid import UUID, uuid4

from common.application.command import Command, CommandHandler
from common.application.ports.file_storage import FileStorage
from common.application.uow import UnitOfWork
from users.application.ports.repo import UserRepo


@dataclass(frozen=True)
class UpdateAvatar(Command[str]):
    user_id: UUID
    file: BytesIO
    filename: str


@dataclass
class UpdateAvatarHandler(CommandHandler[UpdateAvatar, str]):
    _user_repo: UserRepo
    _file_storage: FileStorage
    _uow: UnitOfWork

    async def __call__(self, command: UpdateAvatar) -> str:
        file_name = f"/imgs/users/{command.user_id}/avatar/{uuid4()}_{command.filename}"

        await self._file_storage.upload_file(file=command.file, file_name=file_name)
        await self._user_repo.update_user(values=dict(image=file_name), filters=dict(id=command.user_id))
        await self._uow.commit()
        return file_name
