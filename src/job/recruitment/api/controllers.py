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
from job.common.application.dto import EmploymentTypeDTO, SkillDTO, WorkFormatDTO, WorkScheduleDTO
from job.common.application.exceptions import VacancyIdNotExistError
from job.common.application.queries.get_employment_types import GetEmploymentTypesHandler
from job.common.application.queries.get_skills import GetSkillsHandler
from job.common.application.queries.get_vacancies import GetVacanciesHandler, GetVacanciesQuery
from job.common.application.queries.get_vacancy_by_id import GetVacancyByIdHandler
from job.common.application.queries.get_work_formats import GetWorkFormatsHandler
from job.common.application.queries.get_work_schudules import GetWorkSchedulesHandler
from job.employment.api.schemas import GetVacanciesFilters
from job.recruitment.api.schemas import (
    CreateRecruiterSchema,
    CreateVacancySchema,
    UpdateVacancySchema,
    create_recruiter_dto,
    create_vacancy_dto,
)
from job.recruitment.application.commands.create_recruiter import CreateRecruiterHandler
from job.recruitment.application.commands.create_vacancy import CreateVacancyHandler
from job.recruitment.application.commands.delete_vacancy import DeleteVacancyHandler
from job.recruitment.application.commands.edit_vacancy import UpdateVacancyHandler
from job.recruitment.application.dto import (
    DetailedVacancyDTO,
    VacancyDTO,
)
from job.recruitment.application.exceptions import EmptyEmploymentTypesError, EmptySkillsError, EmptyWorkSchedulesError


class VacancyController(Controller):
    exception_handlers: ClassVar[Mapping] = {  # type: ignore  # noqa: PGH003
        EmptySkillsError: error_handler(status_codes.HTTP_400_BAD_REQUEST),
        EmptyEmploymentTypesError: error_handler(status_codes.HTTP_400_BAD_REQUEST),
        EmptyWorkSchedulesError: error_handler(status_codes.HTTP_400_BAD_REQUEST),
        VacancyIdNotExistError: error_handler(status_codes.HTTP_404_NOT_FOUND),
    }
    prefix = "/vacancies"

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
        "/{vacancy_id:uuid}",
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
        "/{vacancy_id:uuid}",
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
