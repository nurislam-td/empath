from collections.abc import Mapping
from typing import ClassVar
from uuid import UUID

from dishka import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import Controller, Request, Response, delete, get, patch, post, status_codes
from litestar.datastructures import State
from litestar.di import Provide
from litestar.dto import DTOData

from auth.api.schemas import JWTUserPayload
from common.api.exception_handlers import error_handler
from common.application.dto import PaginatedDTO
from common.application.query import PaginationParams
from job.common.application.exceptions import VacancyIdNotExistError
from job.common.application.queries.get_vacancies import GetVacanciesHandler, GetVacanciesQuery
from job.common.application.queries.get_vacancy_responses import GetVacancyResponsesHandler, GetVacancyResponsesQuery
from job.employment.api.schemas import GetVacanciesFilters
from job.employment.application.dto import VacancyResponseDTO
from job.recruitment.api.schemas import (
    ChangeResponseStatusSchema,
    CreateRecruiterSchema,
    CreateVacancySchema,
    UpdateVacancySchema,
    create_recruiter_dto,
    create_vacancy_dto,
)
from job.recruitment.application.commands.change_response_status import ChangeResponseStatusHandler
from job.recruitment.application.commands.create_recruiter import CreateRecruiterHandler
from job.recruitment.application.commands.create_vacancy import CreateVacancyHandler
from job.recruitment.application.commands.delete_vacancy import DeleteVacancyHandler
from job.recruitment.application.commands.edit_vacancy import UpdateVacancyHandler
from job.recruitment.application.dto import (
    DetailedAuthorDTO,
    VacancyDTO,
)
from job.recruitment.application.exceptions import (
    EmptyEmploymentTypesError,
    EmptySkillsError,
    EmptyWorkSchedulesError,
    RecruiterIdNotFoundError,
)
from job.recruitment.application.queries.get_recruiter import GetRecruiterHandler


class VacancyController(Controller):
    exception_handlers: ClassVar[Mapping] = {  # type: ignore  # noqa: PGH003
        EmptySkillsError: error_handler(status_codes.HTTP_400_BAD_REQUEST),
        EmptyEmploymentTypesError: error_handler(status_codes.HTTP_400_BAD_REQUEST),
        EmptyWorkSchedulesError: error_handler(status_codes.HTTP_400_BAD_REQUEST),
        VacancyIdNotExistError: error_handler(status_codes.HTTP_404_NOT_FOUND),
        RecruiterIdNotFoundError: error_handler(status_codes.HTTP_404_NOT_FOUND),
    }

    @post(
        "/vacancies",
        status_code=status_codes.HTTP_201_CREATED,
        dto=create_vacancy_dto,
    )
    @inject
    async def create_vacancy(
        self,
        data: DTOData[CreateVacancySchema],
        create_vacancy: Depends[CreateVacancyHandler],
        request: Request[JWTUserPayload, str, State],
    ) -> Response[str]:
        await create_vacancy(data.create_instance(author_id=request.user.sub))
        return Response(content="", status_code=status_codes.HTTP_201_CREATED)

    @patch(
        "/vacancies/{vacancy_id:uuid}",
        status_code=status_codes.HTTP_200_OK,
    )
    @inject
    async def update_vacancy(
        self,
        vacancy_id: UUID,
        data: UpdateVacancySchema,
        update_vacancy: Depends[UpdateVacancyHandler],
        request: Request[JWTUserPayload, str, State],
    ) -> Response[str]:
        # TODO check author
        await update_vacancy(vacancy_id=vacancy_id, command=data)
        return Response(content="", status_code=status_codes.HTTP_201_CREATED)

    @delete(
        "/vacancies/{vacancy_id:uuid}",
        status_code=status_codes.HTTP_204_NO_CONTENT,
    )
    @inject
    async def delete_vacancy(self, vacancy_id: UUID, delete_vacancy: Depends[DeleteVacancyHandler]) -> None:
        await delete_vacancy(vacancy_id)

    @get("/vacancies", status_code=status_codes.HTTP_200_OK, dependencies={"filters": Provide(GetVacanciesFilters)})
    @inject
    async def get_vacancies(
        self,
        filters: GetVacanciesFilters,
        pagination_params: PaginationParams,
        get_vacancies: Depends[GetVacanciesHandler],
        request: Request[JWTUserPayload, str, State],
    ) -> PaginatedDTO[VacancyDTO]:
        return await get_vacancies(
            query=GetVacanciesQuery(**filters.to_dict(), author_id=request.user.sub), pagination=pagination_params
        )

    @post("/vacancies/author", status_code=status_codes.HTTP_201_CREATED, dto=create_recruiter_dto)
    @inject
    async def create_recruiter(
        self,
        data: DTOData[CreateRecruiterSchema],
        create_recruiter: Depends[CreateRecruiterHandler],
        request: Request[JWTUserPayload, str, State],
    ) -> Response[str]:
        await create_recruiter(command=data.create_instance(id=request.user.sub))
        return Response(content="", status_code=status_codes.HTTP_201_CREATED)

    @get(
        "/vacancies/author",
        status_code=status_codes.HTTP_200_OK,
    )
    @inject
    async def get_recruiter(
        self,
        get_recruiter: Depends[GetRecruiterHandler],
        request: Request[JWTUserPayload, str, State],
    ) -> DetailedAuthorDTO:
        return await get_recruiter(request.user.sub)

    @get("/responses", status_code=status_codes.HTTP_200_OK)
    @inject
    async def get_responses(
        self,
        pagination_params: PaginationParams,
        get_responses: Depends[GetVacancyResponsesHandler],
        request: Request[JWTUserPayload, str, State],
        vacancy_id: UUID | None = None,
    ) -> PaginatedDTO[VacancyResponseDTO]:
        return await get_responses(
            pagination=pagination_params,
            query=GetVacancyResponsesQuery(vacancy_id=vacancy_id, response_author_id=request.user.sub),
        )

    @patch("/responses", status_code=status_codes.HTTP_200_OK)
    @inject
    async def change_response_status(
        self,
        data: ChangeResponseStatusSchema,
        change_response_status: Depends[ChangeResponseStatusHandler],
        request: Request[JWTUserPayload, str, State],
    ) -> Response[str]:  # TODO check the author
        await change_response_status(data)
        return Response(content="", status_code=status_codes.HTTP_200_OK)
