from dataclasses import dataclass
from uuid import UUID

from job.common.infrastructure.repositories.vacancy import AlchemyVacancyReader
from job.recruitment.application.dto import DetailedVacancyDTO


@dataclass(frozen=True, slots=True)
class GetVacancyByIdHandler:
    _reader: AlchemyVacancyReader

    async def __call__(self, vacancy_id: UUID) -> DetailedVacancyDTO:
        return await self._reader.get_vacancy_by_id(vacancy_id)
