from dataclasses import dataclass
from uuid import UUID

from msgspec import UNSET

from common.application.uow import UnitOfWork
from job.recruitment.api.schemas import UpdateVacancySchema
from job.recruitment.application.exceptions import EmptyEmploymentTypesError, EmptySkillsError, EmptyWorkSchedulesError
from job.recruitment.infrastructure.repositories.vacancy import AlchemyVacancyRepo


@dataclass(slots=True)
class UpdateVacancyHandler:
    _repo: AlchemyVacancyRepo
    _uow: UnitOfWork

    async def __call__(self, command: UpdateVacancySchema, vacancy_id: UUID) -> None:
        if command.skills is not UNSET and not command.skills:
            raise EmptySkillsError
        if command.employment_type_ids is not UNSET and not command.employment_type_ids:
            raise EmptyEmploymentTypesError
        if command.work_schedule_ids is not UNSET and not command.work_schedule_ids:
            raise EmptyWorkSchedulesError

        await self._repo.update_vacancy(vacancy_id, command)
        await self._uow.commit()
