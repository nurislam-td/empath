from dataclasses import dataclass

from common.application.uow import UnitOfWork
from job.recruitment.api.schemas import CreateRecruiterSchema
from job.recruitment.infrastructure.repositories.vacancy import AlchemyVacancyRepo


@dataclass(slots=True)
class CreateRecruiterHandler:
    _repo: AlchemyVacancyRepo
    _uow: UnitOfWork

    async def __call__(self, command: CreateRecruiterSchema) -> None:
        await self._repo.create_recruiter(command=command)
        await self._uow.commit()
