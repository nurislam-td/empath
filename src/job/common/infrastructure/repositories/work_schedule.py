from dataclasses import dataclass
from typing import ClassVar
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert

from common.infrastructure.repositories.base import AlchemyReader, AlchemyRepo
from common.infrastructure.repositories.pagination import AlchemyPaginator
from job.common.infrastructure.models import (
    RelVacancyWorkSchedule,
    Skill,
    Vacancy,
)


@dataclass(slots=True)
class WorkScheduleDAO:
    """Vacancy Repo implementation."""

    _vacancy: ClassVar[type[Vacancy]] = Vacancy
    _rel_work_schedule_vacancy: ClassVar[type[RelVacancyWorkSchedule]] = RelVacancyWorkSchedule

    _repo: AlchemyRepo
    _reader: AlchemyReader

    async def map_work_schedules_to_vacancy(self, vacancy_id: UUID, work_schedule_ids: list[UUID]) -> None:
        insert_stmt = insert(self._rel_work_schedule_vacancy).values(
            [{"vacancy_id": vacancy_id, "work_schedule_id": _id} for _id in work_schedule_ids]
        )
        await self._repo.execute(insert_stmt)

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


@dataclass(slots=True)
class AlchemyVacancyReader:
    """Vacancy Reader implementation."""

    _paginator: ClassVar[type[AlchemyPaginator]] = AlchemyPaginator
    _vacancy: ClassVar[type[Vacancy]] = Vacancy
    _skill: ClassVar[type[Skill]] = Skill

    _base: AlchemyReader
