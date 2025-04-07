from collections.abc import Mapping
from typing import ClassVar
from uuid import UUID

from dishka import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import Controller, Request, Response, get, patch, post, status_codes
from litestar.datastructures import State
from litestar.di import Provide
from litestar.dto import DTOData

from auth.api.schemas import JWTUserPayload
from common.api.exception_handlers import error_handler
from common.application.dto import PaginatedDTO
from common.application.query import PaginationParams
from job.common.application.exceptions import VacancyIdNotExistError
from job.common.application.queries.get_vacancies import GetVacanciesHandler, GetVacanciesQuery
from job.employment.api.schemas import (
    CreateCVSchema,
    GetVacanciesFilters,
    ResponseToVacancySchema,
    UpdateCVSchema,
    create_cv_dto,
    response_to_vacancy_dto,
)
from job.employment.application.commands.create_cv import CreateCVHandler
from job.employment.application.commands.response_to_vacancy import ResponseToVacancyHandler
from job.employment.application.commands.update_cv import UpdateCVHandler
from job.recruitment.application.dto import (
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

    @get("/vacancies", status_code=status_codes.HTTP_200_OK, dependencies={"filters": Provide(GetVacanciesFilters)})
    @inject
    async def get_vacancies(
        self,
        filters: GetVacanciesFilters,
        pagination_params: PaginationParams,
        get_vacancies: Depends[GetVacanciesHandler],
    ) -> PaginatedDTO[VacancyDTO]:
        return await get_vacancies(query=GetVacanciesQuery(**filters.to_dict()), pagination=pagination_params)

    @post("/cv", status_code=status_codes.HTTP_201_CREATED, dto=create_cv_dto)
    @inject
    async def create_cv(
        self,
        data: DTOData[CreateCVSchema],
        create_cv: Depends[CreateCVHandler],
        request: Request[JWTUserPayload, str, State],
    ) -> Response[str]:
        await create_cv(data.create_instance(author_id=request.user.sub))
        return Response(content="", status_code=status_codes.HTTP_201_CREATED)

    @patch("/cv/{cv_id:uuid}", status_code=status_codes.HTTP_200_OK)
    @inject
    async def update_cv(
        self,
        cv_id: UUID,
        data: UpdateCVSchema,
        update_cv: Depends[UpdateCVHandler],
        request: Request[JWTUserPayload, str, State],
    ) -> Response[str]:
        # TODO check request user
        await update_cv(data, cv_id)
        return Response(content="", status_code=status_codes.HTTP_200_OK)

    @post(
        "/vacancies/{vacancy_id:uuid}/response",
        status_code=status_codes.HTTP_200_OK,
        dto=response_to_vacancy_dto,
    )
    @inject
    async def response_to_vacancy(
        self,
        vacancy_id: UUID,
        data: DTOData[ResponseToVacancySchema],
        response_to_vacancy: Depends[ResponseToVacancyHandler],
    ) -> Response[str]:
        await response_to_vacancy(data.create_instance(vacancy_id=vacancy_id))
        return Response(content="", status_code=status_codes.HTTP_200_OK)
