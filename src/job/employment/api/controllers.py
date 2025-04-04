from collections.abc import Mapping
from typing import ClassVar
from uuid import UUID

from dishka import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import Controller, get, status_codes
from litestar.di import Provide

from common.api.exception_handlers import error_handler
from common.application.dto import PaginatedDTO
from common.application.query import PaginationParams
from job.common.application.exceptions import VacancyIdNotExistError
from job.common.application.queries.get_vacancies import GetVacanciesHandler, GetVacanciesQuery
from job.common.application.queries.get_vacancy_by_id import GetVacancyByIdHandler
from job.recruitment.application.dto import (
    DetailedVacancyDTO,
    VacancyDTO,
)
from job.recruitment.application.exceptions import EmptyEmploymentTypesError, EmptySkillsError, EmptyWorkSchedulesError


class ResponseController(Controller):
    exception_handlers: ClassVar[Mapping] = {  # type: ignore  # noqa: PGH003
        EmptySkillsError: error_handler(status_codes.HTTP_400_BAD_REQUEST),
        EmptyEmploymentTypesError: error_handler(status_codes.HTTP_400_BAD_REQUEST),
        EmptyWorkSchedulesError: error_handler(status_codes.HTTP_400_BAD_REQUEST),
        VacancyIdNotExistError: error_handler(status_codes.HTTP_404_NOT_FOUND),
    }

    @get("/vacancies", status_code=status_codes.HTTP_200_OK, dependencies={"filters": Provide(GetVacanciesQuery)})
    @inject
    async def get_vacancies(
        self,
        filters: GetVacanciesQuery,
        pagination_params: PaginationParams,
        get_vacancies: Depends[GetVacanciesHandler],
    ) -> PaginatedDTO[VacancyDTO]:
        return await get_vacancies(query=filters, pagination=pagination_params)

    @get("/vacancies/{vacancy_id:uuid}", status_code=status_codes.HTTP_200_OK)
    @inject
    async def get_vacancy_by_id(
        self,
        vacancy_id: UUID,
        get_vacancy_by_id: Depends[GetVacancyByIdHandler],
    ) -> DetailedVacancyDTO:
        return await get_vacancy_by_id(vacancy_id)
