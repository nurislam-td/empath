from collections.abc import Sequence
from typing import TYPE_CHECKING, Protocol
from uuid import UUID

from common.application.dto import PaginatedDTO
from common.application.query import PaginationParams
from job.common.application.dto import EmploymentTypeDTO, SkillDTO, SkillWithWeightDTO, WorkFormatDTO, WorkScheduleDTO
from job.employment.application.dto import CVDTO
from job.recruitment.application.dto import (
    DetailedVacancyDTO,
    VacancyDTO,
)

if TYPE_CHECKING:
    from job.common.application.queries.get_vacancies import GetVacanciesQuery


class VacancyReader(Protocol):
    async def get_vacancies(
        self,
        query: "GetVacanciesQuery",
        pagination: PaginationParams,
    ) -> PaginatedDTO[VacancyDTO]: ...

    async def get_vacancy_by_id(self, vacancy_id: UUID) -> DetailedVacancyDTO: ...
    async def get_skills(self, search: str | None, pagination: PaginationParams) -> PaginatedDTO[SkillDTO]: ...

    async def get_work_schedules(self) -> list[WorkScheduleDTO]: ...
    async def get_employment_types(self) -> list[EmploymentTypeDTO]: ...
    async def get_work_formats(self) -> list[WorkFormatDTO]: ...

    async def get_weights(self, skill_ids: set[UUID]) -> list[SkillWithWeightDTO]: ...

    async def get_cvs(self, include_skills: set[UUID]) -> list[CVDTO]: ...
