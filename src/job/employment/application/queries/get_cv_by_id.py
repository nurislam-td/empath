from dataclasses import dataclass
from uuid import UUID

from job.common.infrastructure.repositories.cv import AlchemyCVReader
from job.employment.application.dto import DetailedCVDTO


@dataclass(frozen=True, slots=True)
class GetCVByIdHandler:
    _reader: AlchemyCVReader

    async def __call__(self, cv_id: UUID) -> DetailedCVDTO:
        return await self._reader.get_cv_by_id(cv_id)
