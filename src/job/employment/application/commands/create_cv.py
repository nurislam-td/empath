from dataclasses import dataclass

from common.application.uow import UnitOfWork
from job.common.infrastructure.repositories.cv import AlchemyCVRepo
from job.employment.api.schemas import CreateCVSchema
from job.recruitment.application.exceptions import EmptyEmploymentTypesError, EmptySkillsError, EmptyWorkSchedulesError


@dataclass(slots=True)
class CreateCVHandler:
    _repo: AlchemyCVRepo
    _uow: UnitOfWork

    async def __call__(self, command: CreateCVSchema) -> None:
        if not command.skills:
            raise EmptySkillsError
        if not command.employment_type_ids:
            raise EmptyEmploymentTypesError
        if not command.work_schedule_ids:
            raise EmptyWorkSchedulesError
        await self._repo.create_cv(command)
        await self._uow.commit()
