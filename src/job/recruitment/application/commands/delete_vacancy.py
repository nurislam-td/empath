from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from common.application.uow import UnitOfWork

if TYPE_CHECKING:
    from job.common.infrastructure.repositories.vacancy import AlchemyVacancyRepo


@dataclass(slots=True, frozen=True)
class DeleteVacancyHandler:
    _repo: "AlchemyVacancyRepo"
    _uow: UnitOfWork

    async def __call__(self, vacancy_id: UUID) -> None:
        await self._repo.delete_vacancy(vacancy_id)
        await self._uow.commit()
