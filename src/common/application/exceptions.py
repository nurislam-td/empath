from dataclasses import dataclass

from common.domain.exceptions import AppError


@dataclass(slots=True, eq=False)
class ApplicationError(AppError):
    @property
    def message(self) -> str:
        return "An application error occurred"
