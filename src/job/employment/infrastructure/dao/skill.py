from dataclasses import dataclass
from typing import ClassVar
from uuid import UUID

from sqlalchemy.dialects.postgresql import insert

from common.infrastructure.repositories.base import AlchemyRepo
from job.common.api.schemas import SkillSchema
from job.common.infrastructure.models import (
    Skill,
)
from job.employment.infrastructure.dao.rel_additional_skill_cv import RelCVAdditionalSkillDAO
from job.employment.infrastructure.dao.rel_skill_cv import RelCVSkillDAO


@dataclass(slots=True)
class SkillDAO:
    _skill: ClassVar[type[Skill]] = Skill

    _rel_skill_cv: RelCVSkillDAO
    _rel_additional_skill_cv: RelCVAdditionalSkillDAO
    _base: AlchemyRepo

    async def create_skills(self, skills: list[SkillSchema]) -> None:
        insert_stmt = insert(self._skill).values([skill.to_dict() for skill in skills]).on_conflict_do_nothing()
        await self._base.execute(insert_stmt)

    async def create_skills_for_cv(self, skills: list[SkillSchema], cv_id: UUID) -> None:
        await self.create_skills(skills)
        await self._rel_skill_cv.map_skills_to_cv(cv_id, [skill.id for skill in skills])

    async def update_skills_for_cv(self, skills: list[SkillSchema], cv_id: UUID) -> None:
        await self._rel_skill_cv.unmap_skills_from_cv(cv_id)
        if not skills:
            return
        await self.create_skills(skills)
        await self._rel_skill_cv.map_skills_to_cv(cv_id, [skill.id for skill in skills])

    async def create_additional_skills_for_cv(self, skills: list[SkillSchema], cv_id: UUID) -> None:
        await self.create_skills(skills)
        await self._rel_additional_skill_cv.map_additional_skills_to_cv(cv_id, [skill.id for skill in skills])

    async def update_additional_skills_for_cv(self, skills: list[SkillSchema], cv_id: UUID) -> None:
        await self._rel_additional_skill_cv.unmap_additional_skills_from_cv(cv_id)
        if not skills:
            return
        await self.create_skills(skills)
        await self._rel_additional_skill_cv.map_additional_skills_to_cv(cv_id, [skill.id for skill in skills])
