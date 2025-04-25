from dataclasses import dataclass
from uuid import UUID

from common.application.dto import DTO


@dataclass(frozen=True, slots=True)
class WorkFormatDTO(DTO):
    name: str
    id: UUID


@dataclass(frozen=True, slots=True)
class SalaryDTO(DTO):
    from_: int
    to: int


@dataclass(frozen=True, slots=True)
class EmploymentTypeDTO(DTO):
    name: str
    id: UUID


@dataclass(frozen=True, slots=True)
class WorkScheduleDTO(DTO):
    name: str
    id: UUID


@dataclass(frozen=True, slots=True)
class SkillDTO(DTO):
    name: str
    id: UUID


@dataclass(frozen=True, slots=True)
class SkillWithWeightDTO(SkillDTO):
    weight: float


@dataclass(frozen=True, slots=True)
class CvAuthorDTO(DTO):
    name: str


@dataclass(frozen=True, slots=True)
class CvWithWeightDTO:
    title: str
    is_visible: bool
    salary: SalaryDTO
    skills: list[str]
    author: CvAuthorDTO

    additional_skills: list[str] | None
    about_me: str | None
    cv_file: str | None
    id: UUID

    weight: float


@dataclass(frozen=True, slots=True)
class RecommendationsDTO(DTO):
    weights: list[SkillWithWeightDTO]
    recommendations: list[CvWithWeightDTO]
