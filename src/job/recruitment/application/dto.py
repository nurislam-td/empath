from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from common.application.dto import DTO
from job.common.application.dto import SalaryDTO
from job.common.domain.enums import EducationEnum, WorkExpEnum, WorkFormatEnum


@dataclass(frozen=True, slots=True)
class AuthorDTO(DTO):
    name: str


@dataclass(frozen=True, slots=True)
class DetailedAuthorDTO(DTO):
    name: str
    about_us: str
    email: str


@dataclass(frozen=True, slots=True)
class VacancyDTO(DTO):
    title: str
    salary: SalaryDTO
    address: str | None
    author: AuthorDTO
    work_exp: WorkExpEnum
    work_schedules: list[str]
    employment_types: list[str]
    work_formats: list[str]
    skills: list[str]
    additional_skills: list[str]
    created_at: datetime
    email: str
    id: UUID


@dataclass(frozen=True, slots=True)
class DetailedVacancyDTO(DTO):
    title: str
    salary: SalaryDTO
    author: DetailedAuthorDTO
    work_exp: WorkExpEnum
    work_schedules: list[str]
    employment_types: list[str]
    work_formats: list[str]
    skills: list[str]
    additional_skills: list[str]
    created_at: datetime
    email: str
    id: UUID
    is_visible: bool
    work_format: WorkFormatEnum
    responsibility: str
    requirements: str
    education: EducationEnum
    additional_description: str | None
    address: str | None
