from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from common.application.dto import PaginatedDTO
from common.application.query import PaginationParams
from job.employment.application.dto import VacancyDTO
from job.employment.infrastructure.repositories.vacancy import AlchemyEmploymentVacancyReader

if TYPE_CHECKING:
    from job.common.application.queries.get_vacancies import GetVacanciesQuery


@dataclass(frozen=True, slots=True)
class GetVacanciesHandler:
    _reader: AlchemyEmploymentVacancyReader

    async def __call__(
        self, query: "GetVacanciesQuery", pagination: PaginationParams, employer_id: UUID
    ) -> PaginatedDTO[VacancyDTO]:
        return await self._reader.get_vacancies(query, pagination=pagination, employer_id=employer_id)
