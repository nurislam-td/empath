import asyncio
from collections.abc import Coroutine
from dataclasses import dataclass
from typing import Any, ClassVar
from uuid import UUID

from msgspec import UNSET
from sqlalchemy import delete, update
from sqlalchemy.dialects.postgresql import insert

from common.application.dto import PaginatedDTO
from common.application.query import PaginationParams
from common.infrastructure.repositories.base import AlchemyReader, AlchemyRepo
from common.infrastructure.repositories.pagination import AlchemyPaginator
from job.common.api.schemas import SkillSchema
from job.common.application.exceptions import CVIdNotExistError
from job.common.infrastructure.mapper import convert_db_to_detailed_cv
from job.common.infrastructure.models import (
    CV,
)
from job.common.infrastructure.repositories import query_builder as qb
from job.common.infrastructure.repositories.employment_type import EmploymentTypeDAO
from job.common.infrastructure.repositories.rel_additional_skill_vacancy import RelVacancyAdditionalSkillDAO
from job.common.infrastructure.repositories.rel_skill_vacancy import RelVacancySkillDAO
from job.common.infrastructure.repositories.skill import SkillDAO
from job.common.infrastructure.repositories.work_exp import WorkExpDAO
from job.common.infrastructure.repositories.work_format import WorkFormatDAO
from job.common.infrastructure.repositories.work_schedule import WorkScheduleDAO
from job.employment.api.schemas import CreateCVSchema, UpdateCVSchema
from job.employment.application.dto import DetailedCVDTO


@dataclass(slots=True)
class AlchemyCVRepo:
    _cv: ClassVar[type[CV]] = CV

    _repo: AlchemyRepo
    _reader: AlchemyReader
    _skill: SkillDAO
    _work_schedule: WorkScheduleDAO
    _work_format: WorkFormatDAO
    _employment_type: EmploymentTypeDAO
    _work_exp: WorkExpDAO

    async def create_cv(self, cv: CreateCVSchema) -> None:
        values = cv.to_dict()
        values.pop("salary")
        values.pop("skills", None)
        values.pop("additional_skills", None)
        values.pop("employment_type_ids", None)
        values.pop("work_schedule_ids", None)
        values.pop("work_formats_id", None)
        values.pop("work_exp", None)
        values["salary_from"] = cv.salary.from_
        values["salary_to"] = cv.salary.to
        await self._repo.execute(insert(self._cv).values(values))

        tasks: list[Coroutine[Any, Any, None]] = [
            self._skill.create_skills_for_cv(cv.skills, cv.id),
            self._employment_type.map_employment_types_to_cv(cv.id, cv.employment_type_ids),
            self._work_schedule.map_work_schedules_to_cv(cv.id, cv.work_schedule_ids),
            self._work_format.map_work_formats_to_cv(cv.id, cv.work_formats_id),
            self._work_exp.create_work_exp(cv_id=cv.id, work_exp=cv.work_exp),
        ]

        if cv.additional_skills is not UNSET and cv.additional_skills:
            s = [SkillSchema(id=skill.id, name=skill.name) for skill in cv.additional_skills]
            tasks.append(self._skill.create_additional_skills_for_cv(s, cv.id))

        await asyncio.gather(*tasks)

    async def update_cv(self, cv_id: UUID, cv: UpdateCVSchema) -> None:
        values = cv.to_dict()
        values.pop("salary", None)
        values.pop("skills", None)
        values.pop("additional_skills", None)
        values.pop("employment_type_ids", None)
        values.pop("work_schedule_ids", None)
        values.pop("work_formats_id", None)
        values.pop("work_exp", None)
        if cv.salary is not UNSET:
            values["salary_from"] = cv.salary.from_
            values["salary_to"] = cv.salary.to

        update_stmt = update(self._cv).where(self._cv.id == cv_id).values(values)
        await self._repo.execute(update_stmt)

        tasks: list[Coroutine[Any, Any, None]] = []
        if cv.skills is not UNSET:
            tasks.append(self._skill.update_additional_skills_for_cv(cv.skills, cv_id))
        if cv.additional_skills is not UNSET:
            s = [SkillSchema(id=skill.id, name=skill.name) for skill in cv.additional_skills]
            tasks.append(self._skill.update_additional_skills_for_cv(s, cv_id))
        if cv.employment_type_ids is not UNSET:
            tasks.append(self._employment_type.update_employment_types_for_cv(cv_id, cv.employment_type_ids))
        if cv.work_schedule_ids is not UNSET:
            tasks.append(self._work_schedule.update_work_schedules_for_cv(cv_id, cv.work_schedule_ids))
        if cv.work_formats_id is not UNSET:
            tasks.append(self._work_format.update_work_formats_for_cv(cv_id, cv.work_formats_id))
        if cv.work_exp is not UNSET:
            tasks.append(self._work_exp.update_work_exp(cv_id, cv.work_exp))

        await asyncio.gather(*tasks)

    async def delete_cv(self, cv_id: UUID) -> None:
        await self._repo.execute(delete(self._cv).where(self._cv.id == cv_id))


@dataclass(slots=True)
class AlchemyCVReader:
    _paginator: ClassVar[type[AlchemyPaginator]] = AlchemyPaginator
    _cv: ClassVar[type[CV]] = CV

    _base: AlchemyReader

    async def get_cv_by_id(self, cv_id: UUID) -> DetailedCVDTO:
        qs = qb.get_cv_qs().where(self._cv.id == cv_id)

        cv = await self._base.fetch_one(qs)
        if cv is None:
            raise CVIdNotExistError(cv_id)

        skills = await self._base.fetch_all(qb.get_cv_skill_qs([cv.id]))
        additional_skills = await self._base.fetch_all(qb.get_cv_additional_skill_qs([cv.id]))
        work_schedules = await self._base.fetch_all(qb.get_cv_work_schedules_qs([cv.id]))
        employment_types = await self._base.fetch_all(qb.get_cv_employment_type_qs([cv_id]))
        work_formats = await self._base.fetch_all(qb.get_cv_work_format_qs([cv.id]))
        work_exp = await self._base.fetch_all(qb.get_cv_work_exp_qs([cv.id]))

        return convert_db_to_detailed_cv(
            cv=cv,
            skills=skills,
            additional_skills=additional_skills,
            work_schedules=work_schedules,
            employment_types=employment_types,
            work_formats=work_formats,
            work_exp=work_exp,
        )
