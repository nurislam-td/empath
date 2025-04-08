from dataclasses import dataclass
from uuid import UUID

from job.recruitment.application.dto import DetailedAuthorDTO
from job.recruitment.infrastructure.repositories.vacancy import AlchemyRecruitmentVacancyReader


@dataclass(frozen=True, slots=True)
class GetRecruiterHandler:
    _reader: AlchemyRecruitmentVacancyReader

    async def __call__(self, recruiter_id: UUID) -> DetailedAuthorDTO:
        return await self._reader.get_recruiter(recruiter_id=recruiter_id)
