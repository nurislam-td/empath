from dataclasses import dataclass
from typing import ClassVar
from uuid import UUID

from sqlalchemy import delete, update
from sqlalchemy.dialects.postgresql import insert

from common.infrastructure.repositories.base import AlchemyRepo
from job.common.infrastructure.models import RelCVVacancy
from job.employment.api.schemas import ResponseToVacancySchema
from job.recruitment.api.schemas import ChangeResponseStatusSchema


@dataclass(slots=True)
class AlchemyRecruitmentVacancyResponseRepo:
    _rel_cv_vacancy: ClassVar[type[RelCVVacancy]] = RelCVVacancy

    _base: AlchemyRepo

    async def response_to_vacancy(self, command: ResponseToVacancySchema) -> None:
        values = command.to_dict()
        await self._base.execute(insert(self._rel_cv_vacancy).values(values))

    async def change_response_status(self, command: ChangeResponseStatusSchema) -> None:
        await self._base.execute(
            update(self._rel_cv_vacancy)
            .where(
                (self._rel_cv_vacancy.cv_id == command.cv_id)
                & (self._rel_cv_vacancy.vacancy_id == command.vacancy_id),
            )
            .values(status=command.status),
        )
