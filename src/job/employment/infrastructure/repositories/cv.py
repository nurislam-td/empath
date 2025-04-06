import asyncio
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, ClassVar
from uuid import UUID

from msgspec import UNSET
from sqlalchemy import delete, update
from sqlalchemy.dialects.postgresql import insert

from common.infrastructure.repositories.base import AlchemyRepo
from job.common.api.schemas import SkillSchema
from job.common.infrastructure.models import CV
from job.employment.api.schemas import CreateCVSchema, UpdateCVSchema
from job.employment.infrastructure.dao.employment_type import EmploymentTypeDAO
from job.employment.infrastructure.dao.skill import SkillDAO
from job.employment.infrastructure.dao.work_exp import WorkExpDAO
from job.employment.infrastructure.dao.work_format import WorkFormatDAO
from job.employment.infrastructure.dao.work_schedule import WorkScheduleDAO

if TYPE_CHECKING:
    from collections.abc import Coroutine


@dataclass(slots=True)
class AlchemyCVRepo:
    _cv: ClassVar[type[CV]] = CV

    _base: AlchemyRepo
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
        await self._base.execute(insert(self._cv).values(values))

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
        await self._base.execute(update_stmt)

        tasks: list[Coroutine[Any, Any, None]] = []
        if cv.skills is not UNSET:
            tasks.append(self._skill.update_skills_for_cv(cv.skills, cv_id))
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
        await self._base.execute(delete(self._cv).where(self._cv.id == cv_id))
