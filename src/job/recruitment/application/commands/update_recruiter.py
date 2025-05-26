from dataclasses import dataclass

from common.application.uow import UnitOfWork
from job.recruitment.api.schemas import UpdateRecruiterSchema
from job.recruitment.infrastructure.repositories.vacancy import AlchemyVacancyRepo


@dataclass(slots=True)
class UpdateRecruiterHandler:
    _repo: AlchemyVacancyRepo
    _uow: UnitOfWork

    async def __call__(self, command: UpdateRecruiterSchema) -> None:
        await self._repo.update_recruiter(command=command)
        await self._uow.commit()
