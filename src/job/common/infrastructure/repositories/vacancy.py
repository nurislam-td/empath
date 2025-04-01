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
from job.recruitment.api.schemas import CreateVacancySchema, UpdateVacancySchema
from job.recruitment.api.schemas import Skill as SkillSchema


@dataclass(slots=True)
class AlchemyVacancyRepo:
    """Vacancy Repo implementation."""

    _vacancy: ClassVar[type[Vacancy]] = Vacancy
    _skill: ClassVar[type[Skill]] = Skill

    _rel_skill_vacancy: ClassVar[type[RelVacancySkill]] = RelVacancySkill
    _rel_additional_skill_vacancy: ClassVar[type[RelVacancyAdditionalSkill]] = RelVacancyAdditionalSkill
    _rel_employment_type_vacancy: ClassVar[type[RelVacancyEmploymentType]] = RelVacancyEmploymentType
    _rel_work_schedule_vacancy: ClassVar[type[RelVacancyWorkSchedule]] = RelVacancyWorkSchedule

    _repo: AlchemyRepo
    _reader: AlchemyReader

    async def create_skills(self, skills: list[SkillSchema]) -> None:
        insert_stmt = insert(self._skill).values([skill.to_dict() for skill in skills]).on_conflict_do_nothing()
        await self._repo.execute(insert_stmt)

    async def map_skills_to_vacancy(self, vacancy_id: UUID, skills_id: list[UUID]) -> None:
        existing_skills_id = await self._reader.fetch_sequence(
            select(self._skill.id).where(self._skill.id.in_(skills_id)),
        )
        insert_stmt = insert(self._rel_skill_vacancy).values(
            [{"vacancy_id": vacancy_id, "skill_id": skill_id} for skill_id in existing_skills_id]
        )
        await self._repo.execute(insert_stmt)

    async def map_additional_skills_to_vacancy(self, vacancy_id: UUID, skills_id: list[UUID]) -> None:
        existing_skills_id = await self._reader.fetch_sequence(
            select(self._skill.id).where(self._skill.id.in_(skills_id)),
        )
        insert_stmt = insert(self._rel_additional_skill_vacancy).values(
            [{"vacancy_id": vacancy_id, "skill_id": skill_id} for skill_id in existing_skills_id]
        )
        await self._repo.execute(insert_stmt)

    async def map_employment_types_to_vacancy(self, vacancy_id: UUID, employment_type_ids: list[UUID]) -> None:
        insert_stmt = insert(self._rel_employment_type_vacancy).values(
            [{"vacancy_id": vacancy_id, "employment_type_id": _id} for _id in employment_type_ids]
        )
        await self._repo.execute(insert_stmt)

    async def map_work_schedules_to_vacancy(self, vacancy_id: UUID, work_schedule_ids: list[UUID]) -> None:
        insert_stmt = insert(self._rel_work_schedule_vacancy).values(
            [{"vacancy_id": vacancy_id, "work_schedule_id": _id} for _id in work_schedule_ids]
        )
        await self._repo.execute(insert_stmt)

    async def create_vacancy(self, vacancy: CreateVacancySchema) -> None:
        values = vacancy.to_dict()
        values.pop("salary")
        values.pop("skills", None)
        values.pop("additional_skills", None)
        values["salary_from"] = vacancy.salary.from_
        values["salary_to"] = vacancy.salary.to
        await self._repo.execute(insert(self._vacancy).values(values))

        first_tasks: list[Coroutine[Any, Any, None]] = []
        second_task: list[Coroutine[Any, Any, None]] = []

        first_tasks.append(self.create_skills(vacancy.skills))
        second_task.append(self.map_skills_to_vacancy(vacancy.id, [skill.id for skill in vacancy.skills]))
        if vacancy.additional_skills is not UNSET and vacancy.additional_skills:
            first_tasks.append(self.create_skills(vacancy.additional_skills))
            second_task.append(
                self.map_additional_skills_to_vacancy(vacancy.id, [skill.id for skill in vacancy.additional_skills])
            )

        first_tasks.append(self.map_employment_types_to_vacancy(vacancy.id, vacancy.employment_type_ids))
        first_tasks.append(self.map_work_schedules_to_vacancy(vacancy.id, vacancy.work_schedule_ids))

        await asyncio.gather(*first_tasks)
        await asyncio.gather(*second_task)

    async def unmap_skills_from_vacancy(self, vacancy_id: UUID) -> None:
        await self._repo.execute(
            delete(self._rel_skill_vacancy).where(self._rel_skill_vacancy.vacancy_id == vacancy_id)
        )

    async def update_skills(self, skills: list[SkillSchema], vacancy_id: UUID) -> None:
        await self.unmap_skills_from_vacancy(vacancy_id)
        if not skills:
            return
        await self.create_skills(skills)
        await self.map_skills_to_vacancy(vacancy_id, [skill.id for skill in skills])

    async def unmap_additional_skills(self, vacancy_id: UUID) -> None:
        await self._repo.execute(
            delete(self._rel_skill_vacancy).where(self._rel_skill_vacancy.vacancy_id == vacancy_id)
        )

    async def update_additional_skills(self, skills: list[SkillSchema], vacancy_id: UUID) -> None:
        await self.unmap_additional_skills(vacancy_id)
        if not skills:
            return
        await self.create_skills(skills)
        await self.map_additional_skills_to_vacancy(vacancy_id, [skill.id for skill in skills])

    async def unmap_employment_types(self, vacancy_id: UUID) -> None:
        await self._repo.execute(
            delete(self._rel_employment_type_vacancy).where(self._rel_employment_type_vacancy.vacancy_id == vacancy_id)
        )

    async def update_employment_types(self, vacancy_id: UUID, employment_type_ids: list[UUID]) -> None:
        await self._repo.execute(
            delete(self._rel_employment_type_vacancy).where(self._rel_employment_type_vacancy.vacancy_id == vacancy_id)
        )
        if not employment_type_ids:
            return
        await self.map_employment_types_to_vacancy(vacancy_id, employment_type_ids)

    async def unmap_work_schedules(self, vacancy_id: UUID) -> None:
        await self._repo.execute(
            delete(self._rel_work_schedule_vacancy).where(self._rel_work_schedule_vacancy.vacancy_id == vacancy_id)
        )

    async def update_work_schedules(self, vacancy_id: UUID, work_schedule_ids: list[UUID]) -> None:
        await self._repo.execute(
            delete(self._rel_work_schedule_vacancy).where(self._rel_work_schedule_vacancy.vacancy_id == vacancy_id)
        )
        if not work_schedule_ids:
            return
        await self.map_work_schedules_to_vacancy(vacancy_id, work_schedule_ids)

    async def update_vacancy(self, vacancy_id: UUID, vacancy: UpdateVacancySchema) -> None:
        values = vacancy.to_dict()
        values.pop("salary")
        values.pop("skills", None)
        values.pop("additional_skills", None)
        if vacancy.salary is not UNSET:
            values["salary_from"] = vacancy.salary.from_
            values["salary_to"] = vacancy.salary.to

        update_stmt = update(self._vacancy).where(self._vacancy.id == vacancy_id).values(values)
        await self._repo.execute(update_stmt)

        tasks: list[Coroutine[Any, Any, None]] = []
        if vacancy.skills is not UNSET:
            tasks.append(self.update_skills(vacancy.skills, vacancy_id))
        if vacancy.additional_skills is not UNSET:
            tasks.append(self.update_additional_skills(vacancy.additional_skills, vacancy_id))
        if vacancy.employment_type_ids is not UNSET:
            tasks.append(self.update_employment_types(vacancy_id, vacancy.employment_type_ids))
        if vacancy.work_schedule_ids is not UNSET:
            tasks.append(self.update_work_schedules(vacancy_id, vacancy.work_schedule_ids))

    async def delete_vacancy(self, vacancy_id: UUID) -> None:
        await self._repo.execute(delete(self._vacancy).where(self._vacancy.id == vacancy_id))


@dataclass(slots=True)
class AlchemyVacancyReader:
    """Vacancy Reader implementation."""

    _paginator: ClassVar[type[AlchemyPaginator]] = AlchemyPaginator
    _vacancy: ClassVar[type[Vacancy]] = Vacancy
    _skill: ClassVar[type[Skill]] = Skill

    _base: AlchemyReader
