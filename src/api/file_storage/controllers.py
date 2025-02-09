import mimetypes
from io import BytesIO
from typing import AsyncIterable

from dishka.integrations.litestar import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import get, status_codes
from litestar.controller import Controller
from litestar.response import Stream

from application.file_storage.queries.download_file import (
    DownloadFile,
    DownloadFileHandler,
)


async def bytes_io_generator(
    bytes_io: BytesIO, chunk_size: int = 1024
) -> AsyncIterable[bytes]:
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
    async def download_file(
        self, filepath: str, download_file: Depends[DownloadFileHandler]
    ) -> Stream:
        query = DownloadFile(filepath=filepath)
        file_bytes = await download_file(query)
        media_type, _ = mimetypes.guess_type(filepath)
        return Stream(bytes_io_generator(file_bytes), media_type=media_type)
