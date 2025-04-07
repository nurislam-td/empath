from dataclasses import dataclass
from typing import ClassVar
from uuid import UUID

from sqlalchemy import delete, update
from sqlalchemy.dialects.postgresql import insert

from common.infrastructure.repositories.base import AlchemyRepo
from job.common.infrastructure.models import RelCVVacancy
from job.employment.api.schemas import ResponseToVacancySchema


@dataclass(slots=True)
class AlchemyVacancyResponseRepo:
    _rel_cv_vacancy: ClassVar[type[RelCVVacancy]] = RelCVVacancy

    _base: AlchemyRepo

    async def response_to_vacancy(self, command: ResponseToVacancySchema) -> None:
        values = command.to_dict()
        await self._base.execute(insert(self._rel_cv_vacancy).values(values))

    async def update_response_to_vacancy(self, command: ResponseToVacancySchema) -> None:
        values = command.to_dict()

        update_stmt = (
            update(self._rel_cv_vacancy).where(self._rel_cv_vacancy.vacancy_id == command.vacancy_id).values(values)
        )
        await self._base.execute(update_stmt)

    async def delete_response_from_vacancy(self, vacancy_id: UUID) -> None:
        await self._base.execute(delete(self._rel_cv_vacancy).where(self._rel_cv_vacancy.vacancy_id == vacancy_id))
