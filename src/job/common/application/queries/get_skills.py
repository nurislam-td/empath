from dataclasses import dataclass

from common.application.dto import PaginatedDTO
from common.application.query import PaginationParams
from job.common.application.ports.repo import VacancyReader
from job.recruitment.application.dto import SkillDTO


@dataclass(frozen=True, slots=True)
class GetSkillsHandler:
    _reader: VacancyReader

    async def __call__(self, search: str | None, pagination: PaginationParams) -> PaginatedDTO[SkillDTO]:
        return await self._reader.get_skills(search, pagination=pagination)
