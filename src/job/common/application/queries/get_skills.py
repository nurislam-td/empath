from dataclasses import dataclass

from common.application.dto import PaginatedDTO
from common.application.query import PaginationParams
from job.common.application.dto import SkillDTO
from job.common.application.ports.repo import VacancyReader


@dataclass(frozen=True, slots=True)
class GetSkillsHandler:
    _reader: VacancyReader

    async def __call__(self, search: str | None, pagination: PaginationParams) -> PaginatedDTO[SkillDTO]:
        return await self._reader.get_skills(search, pagination=pagination)
