from dataclasses import dataclass
from uuid import UUID

from common.application.uow import UnitOfWork
from job.employment.infrastructure.repositories.cv import AlchemyCVRepo


@dataclass(slots=True)
class DeleteCVHandler:
    _repo: AlchemyCVRepo
    _uow: UnitOfWork

    async def __call__(self, cv_id: UUID) -> None:
        await self._repo.delete_cv(cv_id=cv_id)
        await self._uow.commit()
