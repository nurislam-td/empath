from dishka import Provider, Scope, from_context, provide  # type: ignore

from application.common.ports.file_storage import FileStorage
from application.file_storage.queries.download_file import DownloadFileHandler
from config import Settings
from infrastructure.common.adapters.file_storage import S3FileStorage


class FileStorageProvider(Provider):
    scope = Scope.REQUEST
    config = from_context(provides=Settings, scope=Scope.APP)

    file_storage = provide(S3FileStorage, provides=FileStorage)

    download_file = provide(DownloadFileHandler)
