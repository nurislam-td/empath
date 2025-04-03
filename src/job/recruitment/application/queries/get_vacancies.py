from dataclasses import dataclass

from articles.application.dto.article import PaginatedArticleDTO
from common.application.dto import PaginatedDTO
from common.application.query import PaginationParams
from job.common.infrastructure.repositories.vacancy import AlchemyVacancyReader
from job.recruitment.api.schemas import GetVacanciesQuery
from job.recruitment.application.dto import VacancyDTO


@dataclass(frozen=True, slots=True)
class GetVacanciesHandler:
    _reader: AlchemyVacancyReader

    async def __call__(self, query: GetVacanciesQuery, pagination: PaginationParams) -> PaginatedDTO[VacancyDTO]:
        return await self._reader.get_vacancies(query, pagination=pagination)
