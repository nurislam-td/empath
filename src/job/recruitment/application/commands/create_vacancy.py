from dataclasses import dataclass

from common.application.uow import UnitOfWork
from job.common.infrastructure.repositories.vacancy import AlchemyVacancyRepo
from job.recruitment.api.schemas import CreateVacancySchema
from job.recruitment.application.exceptions import EmptyEmploymentTypesError, EmptySkillsError, EmptyWorkSchedulesError


@dataclass(slots=True)
class CreateVacancyHandler:
    _repo: AlchemyVacancyRepo
    _uow: UnitOfWork

    async def __call__(self, command: CreateVacancySchema) -> None:
        if not command.skills:
            raise EmptySkillsError
        if not command.employment_type_ids:
            raise EmptyEmploymentTypesError
        if not command.work_schedule_ids:
            raise EmptyWorkSchedulesError
        await self._repo.create_vacancy(vacancy=command)
        await self._uow.commit()
