from io import BytesIO
from typing import Protocol


class FileStorage(Protocol):
    async def upload_file(self, file: BytesIO, file_name: str) -> None: ...

    async def download_file(self, file_name: str) -> BytesIO: ...
