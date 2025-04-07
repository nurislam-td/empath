from dataclasses import dataclass
from uuid import UUID

from common.application.dto import DTO, PaginatedDTO
from common.application.query import PaginationParams
from job.common.infrastructure.repositories.vacancy_responses import AlchemyVacancyResponseReader
from job.employment.application.dto import VacancyResponseDTO


@dataclass(frozen=True, slots=True)
class GetVacancyResponsesQuery(DTO):
    vacancy_id: UUID | None = None
    response_author_id: UUID | None = None
    vacancy_author_id: UUID | None = None


@dataclass(frozen=True, slots=True)
class GetVacancyResponsesHandler:
    _reader: AlchemyVacancyResponseReader

    async def __call__(
        self,
        query: GetVacancyResponsesQuery,
        pagination: PaginationParams,
    ) -> PaginatedDTO[VacancyResponseDTO]:
        return await self._reader.get_vacancy_responses(query=query, pagination=pagination)
