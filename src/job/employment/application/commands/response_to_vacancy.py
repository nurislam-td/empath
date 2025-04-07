from dataclasses import dataclass

from common.application.uow import UnitOfWork
from job.employment.api.schemas import ResponseToVacancySchema
from job.employment.infrastructure.repositories.response_to_vacancy import AlchemyVacancyResponseRepo


@dataclass(slots=True)
class ResponseToVacancyHandler:
    _repo: AlchemyVacancyResponseRepo
    _uow: UnitOfWork

    async def __call__(self, command: ResponseToVacancySchema) -> None:
        await self._repo.response_to_vacancy(command)
        await self._uow.commit()
