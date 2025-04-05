from dataclasses import dataclass

from job.common.application.ports.repo import VacancyReader
from job.recruitment.application.dto import EmploymentTypeDTO


@dataclass(frozen=True, slots=True)
class GetEmploymentTypesHandler:
    _reader: VacancyReader

    async def __call__(self) -> list[EmploymentTypeDTO]:
        return await self._reader.get_employment_types()
