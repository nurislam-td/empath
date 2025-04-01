import asyncio
from dataclasses import dataclass
from enum import Enum
from typing import Any, ClassVar, Coroutine
from uuid import UUID

from msgspec import UNSET
from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert

from common.api.schemas import BaseStruct
from common.infrastructure.repositories.base import AlchemyReader, AlchemyRepo
from common.infrastructure.repositories.pagination import AlchemyPaginator
from job.common.infrastructure.mapper import convert_db_to_skill
from job.common.infrastructure.models import (
    RelVacancyAdditionalSkill,
    RelVacancyEmploymentType,
    RelVacancySkill,
    RelVacancyWorkSchedule,
    Skill,
    Vacancy,
)
from job.common.infrastructure.repositories.employment_type import EmploymentTypeDAO
from job.common.infrastructure.repositories.rel_additional_skill_vacancy import RelVacancyAdditionalSkillDAO
from job.common.infrastructure.repositories.rel_skill_vacancy import RelVacancySkillDAO
from job.common.infrastructure.repositories.skill import SkillDAO
from job.common.infrastructure.repositories.work_schedule import WorkScheduleDAO
from job.recruitment.api.schemas import CreateVacancySchema, UpdateVacancySchema
from job.recruitment.api.schemas import Skill as SkillSchema


@dataclass(slots=True)
class AlchemyVacancyRepo:
    """Vacancy Repo implementation."""

    _vacancy: ClassVar[type[Vacancy]] = Vacancy

    _repo: AlchemyRepo
    _reader: AlchemyReader
    _skill: SkillDAO
    _rel_additional_skill_vacancy: RelVacancyAdditionalSkillDAO
    _rel_skill_vacancy: RelVacancySkillDAO
    _work_schedule: WorkScheduleDAO
    _employment_type: EmploymentTypeDAO

    async def create_vacancy(self, vacancy: CreateVacancySchema) -> None:
        values = vacancy.to_dict()
        values.pop("salary")
        values.pop("skills", None)
        values.pop("additional_skills", None)
        values.pop("employment_type_ids", None)
        values.pop("work_schedule_ids", None)
        values["salary_from"] = vacancy.salary.from_
        values["salary_to"] = vacancy.salary.to
        await self._repo.execute(insert(self._vacancy).values(values))

        tasks: list[Coroutine[Any, Any, None]] = [
            self._skill.create_skills_for_vacancy(vacancy.skills, vacancy.id),
            self._employment_type.map_employment_types_to_vacancy(vacancy.id, vacancy.employment_type_ids),
            self._work_schedule.map_work_schedules_to_vacancy(vacancy.id, vacancy.work_schedule_ids),
        ]

        if vacancy.additional_skills is not UNSET and vacancy.additional_skills:
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
        if vacancy.salary is not UNSET:
            values["salary_from"] = vacancy.salary.from_
            values["salary_to"] = vacancy.salary.to

        update_stmt = update(self._vacancy).where(self._vacancy.id == vacancy_id).values(values)
        await self._repo.execute(update_stmt)

        tasks: list[Coroutine[Any, Any, None]] = []
        if vacancy.skills is not UNSET:
            tasks.append(self._skill.update_skills(vacancy.skills, vacancy_id))
        if vacancy.additional_skills is not UNSET:
            s = [SkillSchema(id=skill.id, name=skill.name) for skill in vacancy.additional_skills]
            tasks.append(self._skill.update_additional_skills(s, vacancy_id))
        if vacancy.employment_type_ids is not UNSET:
            tasks.append(self._employment_type.update_employment_types(vacancy_id, vacancy.employment_type_ids))
        if vacancy.work_schedule_ids is not UNSET:
            tasks.append(self._work_schedule.update_work_schedules(vacancy_id, vacancy.work_schedule_ids))
        await asyncio.gather(*tasks)

    async def delete_vacancy(self, vacancy_id: UUID) -> None:
        await self._repo.execute(delete(self._vacancy).where(self._vacancy.id == vacancy_id))


@dataclass(slots=True)
class AlchemyVacancyReader:
    """Vacancy Reader implementation."""

    _paginator: ClassVar[type[AlchemyPaginator]] = AlchemyPaginator
    _vacancy: ClassVar[type[Vacancy]] = Vacancy
    _skill: ClassVar[type[Skill]] = Skill

    _base: AlchemyReader
