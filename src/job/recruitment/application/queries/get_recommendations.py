from dataclasses import dataclass
from uuid import UUID

from job.common.application.dto import CvWithWeightDTO, RecommendationsDTO
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
                **cv.to_dict(),
                weight=sum(weight_map.get(skill, 0.0) for skill in cv.skills),
            )
            for cv in cvs
        ]

        recommendations = sorted(recommendations, key=lambda x: x.weight, reverse=True)[:10]
        return RecommendationsDTO(
            recommendations=recommendations,
            weights=skill_weights,
        )
