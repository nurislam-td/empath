import asyncio
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, ClassVar
from uuid import UUID

from msgspec import UNSET
from sqlalchemy import delete, update
from sqlalchemy.dialects.postgresql import insert

from common.infrastructure.repositories.base import AlchemyReader, AlchemyRepo
from job.common.infrastructure.models import (
    Recruiter,
    Vacancy,
)
from job.recruitment.api.schemas import (
    CreateRecruiterSchema,
    CreateVacancySchema,
    UpdateVacancySchema,
)
from job.recruitment.infrastructure.dao.employment_type import EmploymentTypeDAO
from job.recruitment.infrastructure.dao.rel_additional_skill_vacancy import RelVacancyAdditionalSkillDAO
from job.recruitment.infrastructure.dao.rel_skill_vacancy import RelVacancySkillDAO
from job.recruitment.infrastructure.dao.skill import SkillDAO
from job.recruitment.infrastructure.dao.work_format import WorkFormatDAO
from job.recruitment.infrastructure.dao.work_schedule import WorkScheduleDAO

if TYPE_CHECKING:
    from collections.abc import Coroutine


@dataclass(slots=True)
class AlchemyVacancyRepo:
    """Vacancy Repo implementation."""

    _vacancy: ClassVar[type[Vacancy]] = Vacancy
    _recruiter: ClassVar[type[Recruiter]] = Recruiter

    _repo: AlchemyRepo
    _reader: AlchemyReader
    _skill: SkillDAO
    _rel_additional_skill_vacancy: RelVacancyAdditionalSkillDAO
    _rel_skill_vacancy: RelVacancySkillDAO
    _work_schedule: WorkScheduleDAO
    _work_format: WorkFormatDAO
    _employment_type: EmploymentTypeDAO

    async def create_vacancy(self, vacancy: CreateVacancySchema) -> None:
        values = vacancy.to_dict()
        values.pop("salary")
        values.pop("skills", None)
        values.pop("additional_skills", None)
        values.pop("employment_type_ids", None)
        values.pop("work_schedule_ids", None)
        values.pop("work_formats_id", None)
        values["salary_from"] = vacancy.salary.from_
        values["salary_to"] = vacancy.salary.to
        await self._repo.execute(insert(self._vacancy).values(values))

        tasks: list[Coroutine[Any, Any, None]] = [
            self._skill.create_skills_for_vacancy(vacancy.skills, vacancy.id),
            self._employment_type.map_employment_types_to_vacancy(vacancy.id, vacancy.employment_type_ids),
            self._work_schedule.map_work_schedules_to_vacancy(vacancy.id, vacancy.work_schedule_ids),
            self._work_format.map_work_format_to_vacancy(vacancy.id, vacancy.work_formats_id),
        ]

        if vacancy.additional_skills is not UNSET and vacancy.additional_skills:
            from job.common.api.schemas import SkillSchema

            s = [SkillSchema(id=skill.id, name=skill.name) for skill in vacancy.additional_skills]
            tasks.append(self._skill.create_additional_skills_for_vacancy(s, vacancy.id))

        await asyncio.gather(*tasks)

    async def update_vacancy(self, vacancy_id: UUID, vacancy: UpdateVacancySchema) -> None:
        values = vacancy.to_dict()
        values.pop("salary", None)
        values.pop("skills", None)
        values.pop("additional_skills", None)
        values.pop("employment_type_ids", None)
        values.pop("work_schedule_ids", None)
        values.pop("work_formats_id", None)
        if vacancy.salary is not UNSET:
            values["salary_from"] = vacancy.salary.from_
            values["salary_to"] = vacancy.salary.to

        update_stmt = update(self._vacancy).where(self._vacancy.id == vacancy_id).values(values)
        await self._repo.execute(update_stmt)

        tasks: list[Coroutine[Any, Any, None]] = []
        if vacancy.skills is not UNSET:
            tasks.append(self._skill.update_skills(vacancy.skills, vacancy_id))
        if vacancy.additional_skills is not UNSET:
            from job.common.api.schemas import SkillSchema

            s = [SkillSchema(id=skill.id, name=skill.name) for skill in vacancy.additional_skills]
            tasks.append(self._skill.update_additional_skills(s, vacancy_id))
        if vacancy.employment_type_ids is not UNSET:
            tasks.append(self._employment_type.update_employment_types(vacancy_id, vacancy.employment_type_ids))
        if vacancy.work_schedule_ids is not UNSET:
            tasks.append(self._work_schedule.update_work_schedules(vacancy_id, vacancy.work_schedule_ids))
        if vacancy.work_formats_id is not UNSET:
            tasks.append(self._work_format.update_work_format(vacancy_id, vacancy.work_formats_id))

        await asyncio.gather(*tasks)

    async def delete_vacancy(self, vacancy_id: UUID) -> None:
        await self._repo.execute(delete(self._vacancy).where(self._vacancy.id == vacancy_id))

    async def create_recruiter(self, command: CreateRecruiterSchema) -> None:
        insert_stmt = insert(self._recruiter).values(command.to_dict())
        await self._repo.execute(insert_stmt)
