from dataclasses import dataclass
from uuid import UUID

from common.application.uow import UnitOfWork
from job.employment.api.schemas import UpdateCVSchema
from job.employment.infrastructure.repositories.cv import AlchemyCVRepo
from job.recruitment.application.exceptions import EmptyEmploymentTypesError, EmptySkillsError, EmptyWorkSchedulesError


@dataclass(slots=True)
class UpdateCVHandler:
    _repo: AlchemyCVRepo
    _uow: UnitOfWork

    async def __call__(self, command: UpdateCVSchema, cv_id: UUID) -> None:
        if not command.skills:
            raise EmptySkillsError
        if not command.employment_type_ids:
            raise EmptyEmploymentTypesError
        if not command.work_schedule_ids:
            raise EmptyWorkSchedulesError
        await self._repo.update_cv(cv=command, cv_id=cv_id)
        await self._uow.commit()
