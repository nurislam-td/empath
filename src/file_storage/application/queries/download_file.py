from dataclasses import dataclass
from io import BytesIO

from common.application.ports.file_storage import FileStorage
from common.application.query import Query, QueryHandler


@dataclass(frozen=True)
class DownloadFile(Query[BytesIO]):
    filepath: str


@dataclass
class DownloadFileHandler(QueryHandler[DownloadFile, BytesIO]):
    _file_storage: FileStorage

    async def __call__(self, query: DownloadFile) -> BytesIO:
        return await self._file_storage.download_file(query.filepath)
