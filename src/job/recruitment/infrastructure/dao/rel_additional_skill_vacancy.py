from dataclasses import dataclass
from typing import ClassVar
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert

from common.infrastructure.repositories.base import AlchemyReader, AlchemyRepo
from job.common.infrastructure.models import (
    RelVacancyAdditionalSkill,
    Skill,
)


@dataclass(slots=True)
class RelVacancyAdditionalSkillDAO:
    _skill: ClassVar[type[Skill]] = Skill
    _rel_additional_skill_vacancy: ClassVar[type[RelVacancyAdditionalSkill]] = RelVacancyAdditionalSkill

    _repo: AlchemyRepo
    _reader: AlchemyReader

    async def map_additional_skills_to_vacancy(self, vacancy_id: UUID, skills_id: list[UUID]) -> None:
        existing_skills_id = await self._reader.fetch_sequence(
            select(self._skill.id).where(self._skill.id.in_(skills_id)),
        )
        insert_stmt = insert(self._rel_additional_skill_vacancy).values(
            [{"vacancy_id": vacancy_id, "skill_id": skill_id} for skill_id in existing_skills_id]
        )
        await self._repo.execute(insert_stmt)

    async def unmap_additional_skills(self, vacancy_id: UUID) -> None:
        await self._repo.execute(
            delete(self._rel_additional_skill_vacancy).where(
                self._rel_additional_skill_vacancy.vacancy_id == vacancy_id
            )
        )
