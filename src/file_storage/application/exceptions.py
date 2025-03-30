from common.application.exceptions import ApplicationError


class FileNotExistError(ApplicationError):
    @property
    def message(self) -> str:
        return "File not found"


class FileUploadError(ApplicationError):
    @property
    def message(self) -> str:
        return "File upload error"
