from dataclasses import dataclass
from typing import ClassVar
from uuid import UUID

from sqlalchemy import delete, insert

from common.infrastructure.repositories.base import AlchemyRepo
from job.common.infrastructure.models import WorkExp
from job.employment.api.schemas import WorkExpSchema


@dataclass(frozen=True, slots=True)
class WorkExpDAO:
    _work_exp: ClassVar[type[WorkExp]] = WorkExp
    _base: AlchemyRepo

    async def create_work_exp(self, cv_id: UUID, work_exp: list[WorkExpSchema]) -> None:
        insert_stmt = insert(self._work_exp).values([exp.to_dict() | {"cv_id": cv_id} for exp in work_exp])
        await self._base.execute(insert_stmt)

    async def delete_work_exp(self, cv_id: UUID) -> None:
        await self._base.execute(delete(self._work_exp).where(self._work_exp.cv_id == cv_id))

    async def update_work_exp(self, cv_id: UUID, work_exp: list[WorkExpSchema]) -> None:
        await self.delete_work_exp(cv_id)
        await self.create_work_exp(cv_id, work_exp)
