from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from common.application.dto import PaginatedDTO
from common.application.query import PaginationParams
from common.infrastructure.repositories.base import AlchemyReader
from common.infrastructure.repositories.pagination import AlchemyPaginator
from job.common.infrastructure.mapper import convert_db_to_vacancy_responses
from job.common.infrastructure.models import (
    RelCVVacancy,
    Skill,
    Vacancy,
)
from job.common.infrastructure.query_builders import vacancy_responses as qb
from job.employment.application.dto import VacancyResponseDTO

if TYPE_CHECKING:
    from job.common.application.queries.get_vacancy_responses import GetVacancyResponsesQuery


@dataclass(slots=True)
class AlchemyVacancyResponseReader:
    _paginator: ClassVar[type[AlchemyPaginator]] = AlchemyPaginator
    _vacancy: ClassVar[type[Vacancy]] = Vacancy
    _cv: ClassVar[type[Skill]] = Skill
    _rel_cv_vacancy: ClassVar[type[RelCVVacancy]] = RelCVVacancy

    _base: AlchemyReader

    async def get_vacancy_responses(
        self,
        query: "GetVacancyResponsesQuery",
        pagination: PaginationParams,
    ) -> PaginatedDTO[VacancyResponseDTO]:
        qs = qb.get_vacancy_responses_qs(
            filters=query,
        )

        value_count = await self._base.count(qs)
        qs = self._paginator.paginate(qs, pagination.page, pagination.per_page)

        vacancy_responses = await self._base.fetch_all(qs)
        if not vacancy_responses:
            return PaginatedDTO[VacancyResponseDTO](count=value_count, page=pagination.page, results=[])

        return PaginatedDTO[VacancyResponseDTO](
            count=value_count,
            page=pagination.page,
            results=[convert_db_to_vacancy_responses(i) for i in vacancy_responses],
        )
