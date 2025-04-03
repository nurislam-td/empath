from dataclasses import dataclass

from common.application.dto import PaginatedDTO
from common.application.query import PaginationParams
from job.common.infrastructure.repositories.vacancy import AlchemyVacancyReader
from job.recruitment.application.dto import SkillDTO


@dataclass(frozen=True, slots=True)
class GetSkillsHandler:
    _reader: AlchemyVacancyReader

    async def __call__(self, search: str, pagination: PaginationParams) -> PaginatedDTO[SkillDTO]:
        return await self._reader.get_skills(search, pagination=pagination)
