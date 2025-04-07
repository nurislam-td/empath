from dataclasses import dataclass
from uuid import UUID

from common.application.dto import PaginatedDTO
from common.application.query import PaginationParams
from job.employment.application.dto import CVDTO
from job.employment.infrastructure.repositories.cv import AlchemyEmploymentCVReader


@dataclass(frozen=True, slots=True)
class GetCvListHandler:
    _reader: AlchemyEmploymentCVReader

    async def __call__(self, pagination: PaginationParams, employer_id: UUID) -> PaginatedDTO[CVDTO]:
        return await self._reader.get_cv_list(pagination=pagination, employer_id=employer_id)
