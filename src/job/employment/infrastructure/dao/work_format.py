from dataclasses import dataclass
from typing import ClassVar
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert

from common.infrastructure.repositories.base import AlchemyRepo
from job.common.infrastructure.models import RelCVWorkFormat


@dataclass(slots=True)
class WorkFormatDAO:
    _rel_work_format_cv: ClassVar[type[RelCVWorkFormat]] = RelCVWorkFormat

    _base: AlchemyRepo

    async def map_work_formats_to_cv(self, cv_id: UUID, work_formats_id: list[UUID]) -> None:
        insert_stmt = insert(self._rel_work_format_cv).values(
            [{"cv_id": cv_id, "work_format_id": _id} for _id in work_formats_id]
        )
        await self._base.execute(insert_stmt)

    async def unmap_work_formats_from_cv(self, cv_id: UUID) -> None:
        await self._base.execute(
            delete(self._rel_work_format_cv).where(self._rel_work_format_cv.cv_id == cv_id),
        )

    async def update_work_formats_for_cv(self, cv_id: UUID, work_formats_ids: list[UUID]) -> None:
        await self.unmap_work_formats_from_cv(cv_id)
        if not work_formats_ids:
            return
        await self.map_work_formats_to_cv(cv_id, work_formats_ids)
