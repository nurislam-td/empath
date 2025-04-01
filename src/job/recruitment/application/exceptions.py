from dataclasses import dataclass

from common.application.exceptions import ApplicationError


@dataclass(slots=True, eq=False)
class ContentAuthorMismatchError(ApplicationError):
    @property
    def message(self) -> str:
        return "You are not the author of this content"


@dataclass(slots=True, eq=False)
class EmptySkillsError(ApplicationError):
    @property
    def message(self) -> str:
        return "Empty skills list"


@dataclass(slots=True, eq=False)
class EmptyEmploymentTypesError(ApplicationError):
    @property
    def message(self) -> str:
        return "Empty employment type list"


@dataclass(slots=True, eq=False)
class EmptyWorkSchedulesError(ApplicationError):
    @property
    def message(self) -> str:
        return "Empty work schedule list"
