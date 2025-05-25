import heapq
from dataclasses import dataclass
from functools import partial
from uuid import UUID

from job.common.application.dto import CvAuthorDTO, CvWithWeightDTO, RecommendationsDTO, SkillNameWeightDTO
from job.common.application.ports.repo import VacancyReader
from job.employment.application.dto import CVDTO


@dataclass(frozen=True, slots=True)
class GetRecommendationsHandler:
    _reader: VacancyReader

    def _get_cv_weight(self, cv: CVDTO, weight_map: dict[str, float]) -> float:
        all_skills = set(cv.skills) | set(cv.additional_skills or ())
        all_skills = {s for s in all_skills if s in weight_map}
        return sum(weight_map.get(s, 0.0) for s in all_skills) / len(all_skills) if all_skills else 0.0

    async def __call__(self, vacancy_id: UUID) -> RecommendationsDTO:
        vacancy = await self._reader.get_vacancy_by_id(vacancy_id=vacancy_id)
        skill_ids = {d.id for d in vacancy.skills}

        skill_weights = await self._reader.get_weights(skill_ids)
        weight_map = {weight.name: weight.weight for weight in skill_weights}

        cvs = await self._reader.get_cvs(include_skills=skill_ids)

        calculate_cv_weight = partial(self._get_cv_weight, weight_map=weight_map)
        top_cvs = heapq.nlargest(10, cvs, key=calculate_cv_weight)

        recommendations: list[CvWithWeightDTO] = []
        for cv in top_cvs:
            w = calculate_cv_weight(cv)
            skills_dto = [SkillNameWeightDTO(name=s, weight=weight_map.get(s, 0.0)) for s in cv.skills]
            add_skills = cv.additional_skills or []
            additional_dto = [SkillNameWeightDTO(name=s, weight=weight_map.get(s, 0.0)) for s in add_skills] or None

            recommendations.append(
                CvWithWeightDTO(
                    title=cv.title,
                    is_visible=cv.is_visible,
                    salary=cv.salary,
                    skills=skills_dto,
                    author=CvAuthorDTO(name=cv.author.name, email=cv.author.email),
                    additional_skills=additional_dto,
                    about_me=cv.about_me,
                    cv_file=cv.cv_file,
                    id=cv.id,
                    weight=w,
                ),
            )

        return RecommendationsDTO(recommendations=recommendations, weights=skill_weights)
