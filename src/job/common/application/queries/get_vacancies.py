from dataclasses import dataclass
from uuid import UUID

from common.application.dto import DTO, PaginatedDTO
from common.application.query import PaginationParams
from job.common.application.ports.repo import VacancyReader
from job.common.domain.enums import EducationEnum, WorkExpEnum, WorkFormatEnum
from job.recruitment.application.dto import VacancyDTO


@dataclass(frozen=True, slots=True)
class GetVacanciesQuery(DTO):
    salary_from: int | None = None
    salary_to: int | None = None
    work_exp: list[WorkExpEnum] | None = None
    education: list[EducationEnum] | None = None
    work_format: list[WorkFormatEnum] | None = None
    exclude_word: list[str] | None = None
    include_word: list[str] | None = None
    search: str | None = None
    author_id: UUID | None = None


@dataclass(frozen=True, slots=True)
class GetVacanciesHandler:
    _reader: VacancyReader

    async def __call__(self, query: GetVacanciesQuery, pagination: PaginationParams) -> PaginatedDTO[VacancyDTO]:
        return await self._reader.get_vacancies(query, pagination=pagination)
