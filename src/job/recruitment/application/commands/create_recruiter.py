from dataclasses import dataclass

from common.application.uow import UnitOfWork
from job.common.infrastructure.repositories.vacancy import AlchemyVacancyRepo
from job.recruitment.api.schemas import CreateRecruiterSchema


@dataclass(slots=True)
class CreateRecruiterHandler:
    _repo: AlchemyVacancyRepo
    _uow: UnitOfWork

    async def __call__(self, command: CreateRecruiterSchema) -> None:
        await self._repo.create_recruiter(command=command)
        await self._uow.commit()
