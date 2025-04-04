from dataclasses import dataclass

from job.common.infrastructure.repositories.vacancy import AlchemyVacancyReader
from job.recruitment.application.dto import EmploymentTypeDTO


@dataclass(frozen=True, slots=True)
class GetEmploymentTypesHandler:
    _reader: AlchemyVacancyReader

    async def __call__(self) -> list[EmploymentTypeDTO]:
        return await self._reader.get_employment_types()
