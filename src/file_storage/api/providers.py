from dishka import Provider, Scope, from_context, provide  # type: ignore  # noqa: PGH003

from common.application.ports.file_storage import FileStorage
from common.infrastructure.adapters.file_storage import S3FileStorage
from config import Settings
from file_storage.application.commands.upload_file import UploadFileHandler
from file_storage.application.queries.download_file import DownloadFileHandler


class FileStorageProvider(Provider):
    scope = Scope.REQUEST
    config = from_context(provides=Settings, scope=Scope.APP)

    file_storage = provide(S3FileStorage, provides=FileStorage)

    download_file = provide(DownloadFileHandler)
    upload_file = provide(UploadFileHandler)
