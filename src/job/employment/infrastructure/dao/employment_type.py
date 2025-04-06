from dataclasses import dataclass
from typing import ClassVar
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert

from common.infrastructure.repositories.base import AlchemyReader, AlchemyRepo
from job.common.infrastructure.models import (
    RelCVEmploymentType,
)


@dataclass(slots=True)
class EmploymentTypeDAO:
    _rel_employment_type_cv: ClassVar[type[RelCVEmploymentType]] = RelCVEmploymentType

    _base: AlchemyRepo

    async def map_employment_types_to_cv(self, cv_id: UUID, employment_type_ids: list[UUID]) -> None:
        insert_stmt = insert(self._rel_employment_type_cv).values(
            [{"cv_id": cv_id, "employment_type_id": _id} for _id in employment_type_ids]
        )
        await self._base.execute(insert_stmt)

    async def unmap_employment_types_from_cv(self, cv_id: UUID) -> None:
        await self._base.execute(
            delete(self._rel_employment_type_cv).where(self._rel_employment_type_cv.cv_id == cv_id),
        )

    async def update_employment_types_for_cv(self, cv_id: UUID, employment_type_ids: list[UUID]) -> None:
        await self.unmap_employment_types_from_cv(cv_id)
        if not employment_type_ids:
            return
        await self.map_employment_types_to_cv(cv_id, employment_type_ids)
