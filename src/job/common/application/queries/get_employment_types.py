from dataclasses import dataclass

from job.common.application.dto import EmploymentTypeDTO
from job.common.application.ports.repo import VacancyReader


@dataclass(frozen=True, slots=True)
class GetEmploymentTypesHandler:
    _reader: VacancyReader

    async def __call__(self) -> list[EmploymentTypeDTO]:
        return await self._reader.get_employment_types()
