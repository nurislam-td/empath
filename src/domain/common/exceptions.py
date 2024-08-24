from dataclasses import dataclass
from typing import ClassVar


@dataclass(eq=False, slots=True)
class AppError(Exception):
    """Base Error."""

    status: ClassVar[int] = 500

    @property
    def message(self) -> str:
        return "An app error occurred"


@dataclass(eq=False, slots=True)
class DomainError(AppError):
    """Base Domain Error."""

    @property
    def message(self) -> str:
        return "A domain error occurred"


@dataclass(eq=False, slots=True)
class ValueObjectError(DomainError):
    """Base Value Error"""

    @property
    def message(self) -> str:
        return "A value error occurred"
