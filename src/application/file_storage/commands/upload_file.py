from dataclasses import dataclass
from enum import Enum
from io import BytesIO
from uuid import uuid4

from application.common.command import Command, CommandHandler
from application.common.ports.file_storage import FileStorage
from application.common.uow import UnitOfWork


class StorageNames(str, Enum):
    ARTICLE = "article"


class FileType(str, Enum):
    IMG = "imgs"


@dataclass(frozen=True)
class UploadFile(Command[str]):
    storage_name: StorageNames
    file_type: FileType
    file: BytesIO
    filename: str


@dataclass(slots=True)
class UploadFileHandler(CommandHandler[UploadFile, str]):
    _file_storage: FileStorage
    _uow: UnitOfWork

    async def __call__(self, command: UploadFile) -> str:
        file_name = f"/{command.file_type.value}/{command.storage_name.value}/{uuid4()}_{command.filename}"
        await self._file_storage.upload_file(file=command.file, file_name=file_name)
        await self._uow.commit()
        return file_name
