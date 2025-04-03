from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from common.application.dto import DTO
from job.common.infrastructure.repositories import work_schedule
from job.recruitment.domain.enums import EducationEnum, WorkExpEnum


@dataclass(frozen=True, slots=True)
class SalaryDTO(DTO):
    from_: int
    to: int


@dataclass(frozen=True, slots=True)
class AuthorDTO(DTO):
    name: str


@dataclass(frozen=True, slots=True)
class VacancyDTO(DTO):
    title: str
    salary: SalaryDTO
    address: str
    author: AuthorDTO
    work_exp: WorkExpEnum
    work_schedules: list[str]
    employment_types: list[str]
    skills: list[str]
    additional_skills: list[str]
    created_at: datetime
    email: str
    id: UUID
