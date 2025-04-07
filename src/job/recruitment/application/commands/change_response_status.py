from dataclasses import dataclass

from common.application.uow import UnitOfWork
from job.recruitment.api.schemas import ChangeResponseStatusSchema
from job.recruitment.infrastructure.repositories.response_to_vacancy import AlchemyRecruitmentVacancyResponseRepo


@dataclass(slots=True)
class ChangeResponseStatusHandler:
    _repo: AlchemyRecruitmentVacancyResponseRepo
    _uow: UnitOfWork

    async def __call__(self, command: ChangeResponseStatusSchema) -> None:
        await self._repo.change_response_status(command=command)
        await self._uow.commit()
