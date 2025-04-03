from dataclasses import dataclass
from uuid import UUID

from common.application.exceptions import ApplicationError


@dataclass(slots=True, eq=False)
class VacancyIdNotExistError(ApplicationError):
    vacancy_id: UUID

    @property
    def message(self) -> str:
        return f"Vacancy with that id not exist: {self.vacancy_id}"
