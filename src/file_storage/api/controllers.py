import mimetypes
from collections.abc import AsyncIterable
from io import BytesIO
from typing import Annotated

from dishka.integrations.litestar import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import Response, get, post, status_codes
from litestar.controller import Controller
from litestar.datastructures import UploadFile as LitestarUploadFile
from litestar.enums import RequestEncodingType
from litestar.params import Body
from litestar.response import Stream

from file_storage.application.commands.upload_file import FileType, StorageNames, UploadFile, UploadFileHandler
from file_storage.application.queries.download_file import (
    DownloadFile,
    DownloadFileHandler,
)


async def bytes_io_generator(bytes_io: BytesIO, chunk_size: int = 1024) -> AsyncIterable[bytes]:
    bytes_io.seek(0)

    while chunk := bytes_io.read(chunk_size):
        yield chunk


class FileStorageController(Controller):
    @get(
        path="/{filepath:path}",
        status_code=status_codes.HTTP_200_OK,
        exclude_from_auth=True,
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
    ) -> Response[str]:
        content = await data.read()
        command = UploadFile(
            file_type=file_type,
            storage_name=storage_name,
            file=BytesIO(content),
            filename=data.filename,
        )
        new_url = await upload_file(command)
        return Response(content=new_url, status_code=status_codes.HTTP_200_OK)
