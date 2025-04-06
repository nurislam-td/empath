from dataclasses import dataclass
from typing import ClassVar
from uuid import UUID

from common.infrastructure.repositories.base import AlchemyReader
from common.infrastructure.repositories.pagination import AlchemyPaginator
from job.common.application.exceptions import CVIdNotExistError
from job.common.infrastructure.mapper import convert_db_to_detailed_cv
from job.common.infrastructure.models import CV
from job.common.infrastructure.query_builders import cv as qb
from job.employment.application.dto import DetailedCVDTO


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
