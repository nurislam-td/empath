from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar
from uuid import UUID

import job.common.infrastructure.query_builders.common
from common.application.dto import PaginatedDTO
from common.application.query import PaginationParams
from common.infrastructure.repositories.base import AlchemyReader
from common.infrastructure.repositories.pagination import AlchemyPaginator
from job.common.application.dto import EmploymentTypeDTO, SkillDTO, SkillWithWeightDTO, WorkFormatDTO, WorkScheduleDTO
from job.common.application.exceptions import VacancyIdNotExistError
from job.common.infrastructure.mapper import (
    convert_db_detailed_vacancy,
    convert_db_to_skill_dto,
    convert_db_to_vacancy_list,
)
from job.common.infrastructure.models import (
    Skill,
    Vacancy,
)
from job.common.infrastructure.query_builders import cv as qb_cv
from job.common.infrastructure.query_builders import vacancy as qb
from job.employment.application.dto import CVDTO
from job.employment.infrastructure.mapper import convert_db_to_cv_list
from job.recruitment.application.dto import (
    DetailedVacancyDTO,
    VacancyDTO,
)

if TYPE_CHECKING:
    from job.common.application.queries.get_vacancies import GetVacanciesQuery


@dataclass(slots=True)
class AlchemyVacancyReader:
    _paginator: ClassVar[type[AlchemyPaginator]] = AlchemyPaginator
    _vacancy: ClassVar[type[Vacancy]] = Vacancy
    _skill: ClassVar[type[Skill]] = Skill

    _base: AlchemyReader

    async def get_vacancies(
        self,
        query: "GetVacanciesQuery",
        pagination: PaginationParams,
    ) -> PaginatedDTO[VacancyDTO]:
        qs = qb.get_vacancy_qs(
            filters=query,
            search=query.search,
        )

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

    async def get_vacancy_by_id(self, vacancy_id: UUID) -> DetailedVacancyDTO:
        qs = qb.get_vacancy_qs().where(self._vacancy.id == vacancy_id)

        vacancy = await self._base.fetch_one(qs)
        if vacancy is None:
            raise VacancyIdNotExistError(vacancy_id)

        skills = await self._base.fetch_all(qb.get_vacancy_skill_qs([vacancy.id]))
        additional_skills = await self._base.fetch_all(qb.get_vacancy_additional_skill_qs([vacancy.id]))
        work_schedules = await self._base.fetch_all(qb.get_work_schedules_qs([vacancy.id]))
        employment_types = await self._base.fetch_all(qb.get_employment_type_qs([vacancy_id]))
        work_formats = await self._base.fetch_all(qb.get_work_format_qs([vacancy.id]))

        return convert_db_detailed_vacancy(
            vacancy=vacancy,
            skills=skills,
            additional_skills=additional_skills,
            work_schedules=work_schedules,
            employment_types=employment_types,
            work_formats=work_formats,
        )

    async def get_skills(self, search: str | None, pagination: PaginationParams) -> PaginatedDTO[SkillDTO]:
        qs = job.common.infrastructure.query_builders.common.get_skill_qs(search=search)

        value_count = await self._base.count(qs)
        qs = self._paginator.paginate(qs, pagination.page, pagination.per_page)

        skills = await self._base.fetch_all(qs)

        if not skills:
            return PaginatedDTO[SkillDTO](count=value_count, page=pagination.page, results=[])

        return PaginatedDTO[SkillDTO](
            count=value_count,
            page=pagination.page,
            results=[convert_db_to_skill_dto(skill) for skill in skills],
        )

    async def get_work_schedules(self) -> list[WorkScheduleDTO]:
        qs = qb.get_work_schedules_qs()
        work_schedules = await self._base.fetch_all(qs)
        return [WorkScheduleDTO(id=work_schedule.id, name=work_schedule.name) for work_schedule in work_schedules]

    async def get_employment_types(self) -> list[EmploymentTypeDTO]:
        qs = qb.get_employment_type_qs()
        employment_types = await self._base.fetch_all(qs)
        return [
            EmploymentTypeDTO(id=employment_type.id, name=employment_type.name) for employment_type in employment_types
        ]

    async def get_work_formats(self) -> list[WorkFormatDTO]:
        qs = qb.get_work_format_qs()
        work_formats = await self._base.fetch_all(qs)
        return [WorkFormatDTO(id=work_format.id, name=work_format.name) for work_format in work_formats]

    async def get_weights(self, skill_ids: set[UUID]) -> list[SkillWithWeightDTO]:
        qs = qb.get_weight_qs(skill_ids)
        skills = await self._base.fetch_all(qs)
        return [
            SkillWithWeightDTO(
                id=skill.skill_id,
                name=skill.skill_name,
                weight=skill.idf_smooth,
            )
            for skill in skills
        ]

    async def get_cvs(self, include_skills: set[UUID]) -> list[CVDTO]:
        qs = qb_cv.get_cv_qs()
        qs = qb_cv.filter_cv_skill(qs, include_skills)

        cv = await self._base.fetch_all(qs)
        if not cv:
            return []
        cv_ids = [cv.id for cv in cv]

        skills = await self._base.fetch_all(qb_cv.get_cv_skill_qs(cv_ids))
        additional_skills = await self._base.fetch_all(qb_cv.get_cv_additional_skill_qs(cv_ids))

        return convert_db_to_cv_list(
            cv_list=cv,
            skills=skills,
            additional_skills=additional_skills,
        )
