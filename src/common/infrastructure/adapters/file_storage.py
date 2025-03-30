from collections.abc import Iterable
from io import BytesIO
from typing import Protocol

from botocore.exceptions import ClientError  # type: ignore  # noqa: PGH003

from common.application.ports.file_storage import FileStorage
from config import Settings
from file_storage.application.exceptions import FileNotExistError, FileUploadError


class S3Client(Protocol):
    async def upload_fileobj(self, Fileobj: BytesIO, Bucket: str, Key: str) -> None: ...  # noqa: N803
    async def download_fileobj(self, Bucket: str, Key: str, Fileobj: BytesIO) -> None: ...  # noqa: N803
    async def delete_object(self, Bucket: str, Key: str) -> None: ...  # noqa: N803


class S3FileStorage(FileStorage):
    def __init__(self, client: S3Client, config: Settings) -> None:
        self._client = client
        self._config = config.s3

    async def download_file(self, file_name: str) -> BytesIO:
        file = BytesIO()
        try:
            await self._client.download_fileobj(
                Bucket=self._config.S3_PRIVATE_BUCKET_NAME,
                Key=file_name,
                Fileobj=file,
            )
        except ClientError as e:
            raise FileNotExistError from e
        file.seek(0)
        return file

    async def upload_file(self, file: BytesIO, file_name: str) -> None:
        try:
            await self._client.upload_fileobj(
                Fileobj=file,
                Bucket=self._config.S3_PRIVATE_BUCKET_NAME,
                Key=file_name,
            )
        except Exception as e:
            raise FileUploadError from e

    async def delete_files(self, files: Iterable[str]) -> None:
        for file in files:
            try:
                await self._client.delete_object(
                    Bucket=self._config.S3_PRIVATE_BUCKET_NAME,
                    Key=file,
                )
            except ClientError:
                continue
