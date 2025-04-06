from dataclasses import dataclass
from typing import ClassVar
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert

from common.infrastructure.repositories.base import AlchemyReader, AlchemyRepo
from common.infrastructure.repositories.pagination import AlchemyPaginator
from job.common.infrastructure.models import (
    CV,
    RelCVWorkSchedule,
    RelVacancyWorkSchedule,
    Skill,
    Vacancy,
)


@dataclass(slots=True)
class WorkScheduleDAO:
    _rel_work_schedule_vacancy: ClassVar[type[RelVacancyWorkSchedule]] = RelVacancyWorkSchedule
    _rel_work_schedule_cv: ClassVar[type[RelCVWorkSchedule]] = RelCVWorkSchedule

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

    async def map_work_schedules_to_cv(self, cv_id: UUID, work_schedules_id: list[UUID]) -> None:
        insert_stmt = insert(self._rel_work_schedule_cv).values(
            [{"cv_id": cv_id, "work_schedule_id": _id} for _id in work_schedules_id]
        )
        await self._repo.execute(insert_stmt)

    async def unmap_work_schedules_from_cv(self, cv_id: UUID) -> None:
        await self._repo.execute(
            delete(self._rel_work_schedule_cv).where(self._rel_work_schedule_cv.cv_id == cv_id),
        )

    async def update_work_schedules_for_cv(self, cv_id: UUID, work_schedules_ids: list[UUID]) -> None:
        await self.unmap_work_schedules_from_cv(cv_id)
        if not work_schedules_ids:
            return
        await self.map_work_schedules_to_cv(cv_id, work_schedules_ids)
