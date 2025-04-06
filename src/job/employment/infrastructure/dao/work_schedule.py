from dataclasses import dataclass
from typing import ClassVar
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert

from common.infrastructure.repositories.base import AlchemyRepo
from job.common.infrastructure.models import (
    RelCVWorkSchedule,
)


@dataclass(slots=True)
class WorkScheduleDAO:
    _rel_work_schedule_cv: ClassVar[type[RelCVWorkSchedule]] = RelCVWorkSchedule

    _base: AlchemyRepo

    async def map_work_schedules_to_cv(self, cv_id: UUID, work_schedules_id: list[UUID]) -> None:
        insert_stmt = insert(self._rel_work_schedule_cv).values(
            [{"cv_id": cv_id, "work_schedule_id": _id} for _id in work_schedules_id]
        )
        await self._base.execute(insert_stmt)

    async def unmap_work_schedules_from_cv(self, cv_id: UUID) -> None:
        await self._base.execute(
            delete(self._rel_work_schedule_cv).where(self._rel_work_schedule_cv.cv_id == cv_id),
        )

    async def update_work_schedules_for_cv(self, cv_id: UUID, work_schedules_ids: list[UUID]) -> None:
        await self.unmap_work_schedules_from_cv(cv_id)
        if not work_schedules_ids:
            return
        await self.map_work_schedules_to_cv(cv_id, work_schedules_ids)
