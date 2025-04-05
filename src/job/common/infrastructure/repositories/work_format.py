from dataclasses import dataclass
from typing import ClassVar
from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert

from common.infrastructure.repositories.base import AlchemyReader, AlchemyRepo
from common.infrastructure.repositories.pagination import AlchemyPaginator
from job.common.infrastructure.models import RelVacancyWorkFormat, Skill, Vacancy


@dataclass(slots=True)
class WorkFormatDAO:
    """Vacancy Repo implementation."""

    _vacancy: ClassVar[type[Vacancy]] = Vacancy
    _rel_work_format_vacancy: ClassVar[type[RelVacancyWorkFormat]] = RelVacancyWorkFormat

    _repo: AlchemyRepo

    async def map_work_format_to_vacancy(self, vacancy_id: UUID, work_formats_id: list[UUID]) -> None:
        insert_stmt = insert(self._rel_work_format_vacancy).values(
            [{"vacancy_id": vacancy_id, "work_format_id": _id} for _id in work_formats_id]
        )
        await self._repo.execute(insert_stmt)

    async def unmap_work_format(self, vacancy_id: UUID) -> None:
        await self._repo.execute(
            delete(self._rel_work_format_vacancy).where(self._rel_work_format_vacancy.vacancy_id == vacancy_id)
        )

    async def update_work_format(self, vacancy_id: UUID, work_formats_id: list[UUID]) -> None:
        await self._repo.execute(
            delete(self._rel_work_format_vacancy).where(self._rel_work_format_vacancy.vacancy_id == vacancy_id)
        )
        if not work_formats_id:
            return
        await self.map_work_format_to_vacancy(vacancy_id, work_formats_id)


@dataclass(slots=True)
class AlchemyVacancyReader:
    """Vacancy Reader implementation."""

    _paginator: ClassVar[type[AlchemyPaginator]] = AlchemyPaginator
    _vacancy: ClassVar[type[Vacancy]] = Vacancy
    _skill: ClassVar[type[Skill]] = Skill

    _base: AlchemyReader
