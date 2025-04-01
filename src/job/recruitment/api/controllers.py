from collections.abc import Mapping
from typing import ClassVar
from uuid import UUID

from dishka import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import Controller, Request, Response, delete, patch, post, status_codes
from litestar.datastructures import State
from litestar.dto import DTOData

from auth.api.schemas import JWTUserPayload
from common.api.exception_handlers import error_handler
from job.recruitment.api.schemas import CreateVacancySchema, UpdateVacancySchema, create_vacancy_dto
from job.recruitment.application.commands.create_vacancy import CreateVacancyHandler
from job.recruitment.application.commands.delete_vacancy import DeleteVacancyHandler
from job.recruitment.application.commands.edit_vacancy import UpdateVacancyHandler
from job.recruitment.application.exceptions import EmptyEmploymentTypesError, EmptySkillsError, EmptyWorkSchedulesError


class VacancyController(Controller):
    exception_handlers: ClassVar[Mapping] = {  # type: ignore  # noqa: PGH003
        EmptySkillsError: error_handler(status_codes.HTTP_400_BAD_REQUEST),
        EmptyEmploymentTypesError: error_handler(status_codes.HTTP_400_BAD_REQUEST),
        EmptyWorkSchedulesError: error_handler(status_codes.HTTP_400_BAD_REQUEST),
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
