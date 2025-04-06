from dataclasses import dataclass
from typing import ClassVar
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert

from common.infrastructure.repositories.base import AlchemyRepo
from job.common.infrastructure.models import RelVacancyWorkSchedule


@dataclass(slots=True)
class WorkScheduleDAO:
    _rel_work_schedule_vacancy: ClassVar[type[RelVacancyWorkSchedule]] = RelVacancyWorkSchedule

    _base: AlchemyRepo

    async def map_work_schedules_to_vacancy(self, vacancy_id: UUID, work_schedule_ids: list[UUID]) -> None:
        insert_stmt = insert(self._rel_work_schedule_vacancy).values(
            [{"vacancy_id": vacancy_id, "work_schedule_id": _id} for _id in work_schedule_ids]
        )
        await self._base.execute(insert_stmt)

    async def unmap_work_schedules(self, vacancy_id: UUID) -> None:
        await self._base.execute(
            delete(self._rel_work_schedule_vacancy).where(self._rel_work_schedule_vacancy.vacancy_id == vacancy_id)
        )

    async def update_work_schedules(self, vacancy_id: UUID, work_schedule_ids: list[UUID]) -> None:
        await self._base.execute(
            delete(self._rel_work_schedule_vacancy).where(self._rel_work_schedule_vacancy.vacancy_id == vacancy_id)
        )
        if not work_schedule_ids:
            return
        await self.map_work_schedules_to_vacancy(vacancy_id, work_schedule_ids)
