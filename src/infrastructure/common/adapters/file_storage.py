from io import BytesIO
from typing import Protocol

from application.common.ports.file_storage import FileStorage
from config import Settings


class S3Client(Protocol):
    async def upload_fileobj(self, Fileobj: BytesIO, Bucket: str, Key: str) -> None: ...
    async def download_fileobj(
        self, Bucket: str, Key: str, Fileobj: BytesIO
    ) -> None: ...


class S3FileStorage(FileStorage):
    def __init__(self, client: S3Client, config: Settings) -> None:
        self._client = client
        self._config = config.s3

    async def download_file(self, file_name: str) -> BytesIO:
        file = BytesIO()
        await self._client.download_fileobj(
            Bucket=self._config.S3_PRIVATE_BUCKET_NAME,
            Key=file_name,
            Fileobj=file,
        )
        file.seek(0)
        return file

    async def upload_file(self, file: BytesIO, file_name: str) -> None:
        await self._client.upload_fileobj(
            Fileobj=file,
            Bucket=self._config.S3_PRIVATE_BUCKET_NAME,
            Key=file_name,
        )
