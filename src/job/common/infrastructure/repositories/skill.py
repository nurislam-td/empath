from dataclasses import dataclass
from typing import ClassVar
from uuid import UUID

from sqlalchemy.dialects.postgresql import insert

from common.infrastructure.repositories.base import AlchemyReader, AlchemyRepo
from job.common.infrastructure.models import (
    Skill,
)
from job.common.infrastructure.repositories.rel_additional_skill_vacancy import RelVacancyAdditionalSkillDAO
from job.common.infrastructure.repositories.rel_skill_vacancy import RelVacancySkillDAO
from job.common.api.schemas import SkillSchema as SkillSchema


@dataclass(slots=True)
class SkillDAO:
    """Vacancy Repo implementation."""

    _skill: ClassVar[type[Skill]] = Skill

    _rel_additional_skill_vacancy: RelVacancyAdditionalSkillDAO
    _rel_skill_vacancy: RelVacancySkillDAO

    _repo: AlchemyRepo
    _reader: AlchemyReader

    async def create_skills(self, skills: list[SkillSchema]) -> None:
        insert_stmt = insert(self._skill).values([skill.to_dict() for skill in skills]).on_conflict_do_nothing()
        await self._repo.execute(insert_stmt)

    async def create_skills_for_vacancy(self, skills: list[SkillSchema], vacancy_id: UUID) -> None:
        await self.create_skills(skills)
        await self._rel_skill_vacancy.map_skills_to_vacancy(vacancy_id, [skill.id for skill in skills])

    async def create_additional_skills_for_vacancy(self, skills: list[SkillSchema], vacancy_id: UUID) -> None:
        await self.create_skills(skills)
        await self._rel_additional_skill_vacancy.map_additional_skills_to_vacancy(
            vacancy_id, [skill.id for skill in skills]
        )

    async def update_skills(self, skills: list[SkillSchema], vacancy_id: UUID) -> None:
        await self._rel_skill_vacancy.unmap_skills_from_vacancy(vacancy_id)
        if not skills:
            return
        await self.create_skills(skills)
        await self._rel_skill_vacancy.map_skills_to_vacancy(vacancy_id, [skill.id for skill in skills])

    async def update_additional_skills(self, skills: list[SkillSchema], vacancy_id: UUID) -> None:
        await self._rel_additional_skill_vacancy.unmap_additional_skills(vacancy_id)
        if not skills:
            return
        await self.create_skills(skills)
        await self._rel_additional_skill_vacancy.map_additional_skills_to_vacancy(
            vacancy_id, [skill.id for skill in skills]
        )

    async def create_skills_for_cv(self, skills: list[SkillSchema], cv_id: UUID) -> None:
        await self.create_skills(skills)
        await self._rel
