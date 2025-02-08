from io import BytesIO

from attr import dataclass

from application.common.ports.file_storage import FileStorage
from application.common.query import Query, QueryHandler


@dataclass
class DownloadFile(Query[BytesIO]):
    filepath: str


@dataclass
class DownloadFileHandler(QueryHandler[DownloadFile, BytesIO]):
    _file_storage: FileStorage

    async def __call__(self, query: DownloadFile) -> BytesIO:
        return await self._file_storage.download_file(query.filepath)
