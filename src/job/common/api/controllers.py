from collections.abc import Mapping
from typing import ClassVar
from uuid import UUID

from dishka import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import Controller, get, status_codes

from common.api.exception_handlers import error_handler
from common.application.dto import PaginatedDTO
from common.application.query import PaginationParams
from job.common.application.dto import EmploymentTypeDTO, SkillDTO, WorkFormatDTO, WorkScheduleDTO
from job.common.application.exceptions import VacancyIdNotExistError
from job.common.application.queries.get_employment_types import GetEmploymentTypesHandler
from job.common.application.queries.get_skills import GetSkillsHandler
from job.common.application.queries.get_vacancy_by_id import GetVacancyByIdHandler
from job.common.application.queries.get_work_formats import GetWorkFormatsHandler
from job.common.application.queries.get_work_schedules import GetWorkSchedulesHandler
from job.recruitment.application.dto import DetailedVacancyDTO


class JobController(Controller):
    exception_handlers: ClassVar[Mapping] = {  # type: ignore  # noqa: PGH003
        VacancyIdNotExistError: error_handler(status_codes.HTTP_404_NOT_FOUND),
    }

    @get("/vacancies/{vacancy_id:uuid}", status_code=status_codes.HTTP_200_OK)
    @inject
    async def get_vacancy_by_id(
        self,
        vacancy_id: UUID,
        get_vacancy_by_id: Depends[GetVacancyByIdHandler],
    ) -> DetailedVacancyDTO:
        return await get_vacancy_by_id(vacancy_id)

    @get("/skills", status_code=status_codes.HTTP_200_OK)
    @inject
    async def get_skills(
        self,
        pagination_params: PaginationParams,
        get_skills: Depends[GetSkillsHandler],
        search: str | None = None,
    ) -> PaginatedDTO[SkillDTO]:
        return await get_skills(search=search, pagination=pagination_params)

    @get("/work-schedules", status_code=status_codes.HTTP_200_OK)
    @inject
    async def get_work_schedules(self, get_schedules: Depends[GetWorkSchedulesHandler]) -> list[WorkScheduleDTO]:
        return await get_schedules()

    @get("/employment-types", status_code=status_codes.HTTP_200_OK)
    @inject
    async def get_employment_types(
        self,
        get_employment_types: Depends[GetEmploymentTypesHandler],
    ) -> list[EmploymentTypeDTO]:
        return await get_employment_types()

    @get("/work-formats", status_code=status_codes.HTTP_200_OK)
    @inject
    async def get_work_formats(
        self,
        get_work_formats: Depends[GetWorkFormatsHandler],
    ) -> list[WorkFormatDTO]:
        return await get_work_formats()
