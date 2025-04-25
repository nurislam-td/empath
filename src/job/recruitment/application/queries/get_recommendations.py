from dataclasses import dataclass
from uuid import UUID

from job.common.application.dto import CvAuthorDTO, CvWithWeightDTO, RecommendationsDTO, SkillNameWeightDTO
from job.common.application.ports.repo import VacancyReader


@dataclass(frozen=True, slots=True)
class GetRecommendationsHandler:
    _reader: VacancyReader

    async def __call__(self, vacancy_id: UUID) -> RecommendationsDTO:
        vacancy = await self._reader.get_vacancy_by_id(vacancy_id=vacancy_id)
        skill_ids = {d.id for d in vacancy.skills}

        skill_weights = await self._reader.get_weights(skill_ids)
        weight_map = {weight.name: weight.weight for weight in skill_weights}

        cvs = await self._reader.get_cvs(include_skills=skill_ids)

        recommendations = [
            CvWithWeightDTO(
                title=cv.title,
                is_visible=cv.is_visible,
                salary=cv.salary,
                skills=[SkillNameWeightDTO(name=skill, weight=weight_map.get(skill, 0.0)) for skill in cv.skills],
                author=CvAuthorDTO(name=cv.author.name),
                additional_skills=[
                    SkillNameWeightDTO(name=skill, weight=weight_map.get(skill, 0.0)) for skill in cv.additional_skills
                ]
                if cv.additional_skills
                else None,
                about_me=cv.about_me,
                cv_file=cv.cv_file,
                id=cv.id,
                weight=sum(
                    weight_map.get(skill, 0.0)
                    for skill in cv.skills + (cv.additional_skills if cv.additional_skills else [])
                ),
            )
            for cv in cvs
        ]

        recommendations = sorted(recommendations, key=lambda x: x.weight, reverse=True)[:10]
        return RecommendationsDTO(
            recommendations=recommendations,
            weights=skill_weights,
        )
