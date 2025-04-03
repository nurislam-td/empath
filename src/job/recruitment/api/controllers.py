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
from job.recruitment.api.schemas import (
    CreateVacancySchema,
    GetVacanciesQuery,
    Skill,
    UpdateVacancySchema,
    create_vacancy_dto,
)
from job.recruitment.application.commands.create_vacancy import CreateVacancyHandler
from job.recruitment.application.commands.delete_vacancy import DeleteVacancyHandler
from job.recruitment.application.commands.edit_vacancy import UpdateVacancyHandler
from job.recruitment.application.dto import DetailedVacancyDTO, SkillDTO, VacancyDTO
from job.recruitment.application.exceptions import EmptyEmploymentTypesError, EmptySkillsError, EmptyWorkSchedulesError
from job.recruitment.application.queries.get_skills import GetSkillsHandler
from job.recruitment.application.queries.get_vacancies import GetVacanciesHandler
from job.recruitment.application.queries.get_vacancy_by_id import GetVacancyByIdHandler


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

    @get("/skills", status_code=status_codes.HTTP_200_OK)
    @inject
    async def get_skills(
        self, search: str, pagination_params: PaginationParams, get_skills: Depends[GetSkillsHandler]
    ) -> PaginatedDTO[SkillDTO]:
        return await get_skills(search=search, pagination=pagination_params)
