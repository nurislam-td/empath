import mimetypes
from collections.abc import AsyncIterable, Mapping
from io import BytesIO
from typing import Annotated, ClassVar

from dishka.integrations.litestar import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import get, post, status_codes
from litestar.controller import Controller
from litestar.datastructures import UploadFile as LitestarUploadFile
from litestar.enums import RequestEncodingType
from litestar.params import Body
from litestar.response import Stream

from common.api.exception_handlers import error_handler
from file_storage.api.schema import FileStorageResponse
from file_storage.application.commands.upload_file import FileType, StorageNames, UploadFile, UploadFileHandler
from file_storage.application.exceptions import FileNotExistError
from file_storage.application.queries.download_file import (
    DownloadFile,
    DownloadFileHandler,
)


async def bytes_io_generator(bytes_io: BytesIO, chunk_size: int = 1024) -> AsyncIterable[bytes]:
    bytes_io.seek(0)

    while chunk := bytes_io.read(chunk_size):
        yield chunk


class FileStorageController(Controller):
    exception_handlers: ClassVar[Mapping] = {  # type: ignore  # noqa: PGH003
        FileNotExistError: error_handler(status_codes.HTTP_400_BAD_REQUEST),
    }

    @get(
        path="/{filepath:path}",
        status_code=status_codes.HTTP_200_OK,
    )
    @inject
    async def download_file(self, filepath: str, download_file: Depends[DownloadFileHandler]) -> Stream:
        query = DownloadFile(filepath=filepath)
        file_bytes = await download_file(query)
        media_type, _ = mimetypes.guess_type(filepath)
        return Stream(bytes_io_generator(file_bytes), media_type=media_type)

    @post(
        path="",
        status_code=status_codes.HTTP_200_OK,
    )
    @inject
    async def upload_file(
        self,
        file_type: FileType,
        storage_name: StorageNames,
        data: Annotated[LitestarUploadFile, Body(media_type=RequestEncodingType.MULTI_PART)],
        upload_file: Depends[UploadFileHandler],
    ) -> FileStorageResponse:
        content = await data.read()
        command = UploadFile(
            file_type=file_type,
            storage_name=storage_name,
            file=BytesIO(content),
            filename=data.filename,
        )
        new_url = await upload_file(command)
        return FileStorageResponse(url=new_url)
