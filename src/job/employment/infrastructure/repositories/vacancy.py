from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar
from uuid import UUID

from sqlalchemy import select

from common.application.dto import PaginatedDTO
from common.application.query import PaginationParams
from common.infrastructure.repositories.base import AlchemyReader
from common.infrastructure.repositories.pagination import AlchemyPaginator
from job.common.infrastructure.models import (
    CV,
    RelCVVacancy,
    Vacancy,
)
from job.common.infrastructure.query_builders import vacancy as qb
from job.employment.application.dto import (
    VacancyDTO,
)
from job.employment.infrastructure.mapper import (
    convert_db_to_vacancy_list,
)

if TYPE_CHECKING:
    from job.common.application.queries.get_vacancies import GetVacanciesQuery


@dataclass(slots=True)
class AlchemyEmploymentVacancyReader:
    _paginator: ClassVar[type[AlchemyPaginator]] = AlchemyPaginator
    _vacancy: ClassVar[type[Vacancy]] = Vacancy
    _cv: ClassVar[type[CV]] = CV
    _rel_cv_vacancy: ClassVar[type[RelCVVacancy]] = RelCVVacancy

    _base: AlchemyReader

    def get_vacancy_qs(
        self,
        query: "GetVacanciesQuery",
        employer_id: UUID,
    ) -> qb.Select[qb.Any]:
        qs = qb.get_vacancy_qs(
            filters=query,
            search=query.search,
        )
        responses = (
            select(self._rel_cv_vacancy.vacancy_id, self._rel_cv_vacancy.status)
            .join(
                self._cv.__table__, (self._cv.id == self._rel_cv_vacancy.cv_id) & (self._cv.author_id == employer_id)
            )
            .alias("responses")
        )
        return qs.outerjoin(
            responses,
            responses.c.vacancy_id == self._vacancy.id,
        ).add_columns(responses.c.status)

    async def get_vacancies(
        self,
        query: "GetVacanciesQuery",
        employer_id: UUID,
        pagination: PaginationParams,
    ) -> PaginatedDTO[VacancyDTO]:
        qs = self.get_vacancy_qs(query, employer_id)

        value_count = await self._base.count(qs)
        qs = self._paginator.paginate(qs, pagination.page, pagination.per_page)

        vacancies = await self._base.fetch_all(qs)
        if not vacancies:
            return PaginatedDTO[VacancyDTO](count=value_count, page=pagination.page, results=[])
        vacancies_id = [vacancy.id for vacancy in vacancies]
        skills = await self._base.fetch_all(qb.get_vacancy_skill_qs(vacancies_id))
        additional_skills = await self._base.fetch_all(qb.get_vacancy_additional_skill_qs(vacancies_id))
        work_schedules = await self._base.fetch_all(qb.get_work_schedules_qs(vacancies_id))
        employment_types = await self._base.fetch_all(qb.get_employment_type_qs(vacancies_id))
        work_formats = await self._base.fetch_all(qb.get_work_format_qs(vacancies_id))

        return PaginatedDTO[VacancyDTO](
            count=value_count,
            page=pagination.page,
            results=convert_db_to_vacancy_list(
                vacancies, skills, additional_skills, work_schedules, employment_types, work_formats
            ),
        )
