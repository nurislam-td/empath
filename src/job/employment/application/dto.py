from dataclasses import dataclass
from datetime import date
from uuid import UUID

from common.application.dto import DTO
from job.common.application.dto import EmploymentTypeDTO, SalaryDTO, SkillDTO, WorkFormatDTO, WorkScheduleDTO
from job.common.domain.enums import EducationEnum


@dataclass(frozen=True, slots=True)
class WorkExpDTO(DTO):
    company_name: str
    title: str
    description: str
    start_date: date
    end_date: date | None
    is_relevant: bool


@dataclass(frozen=True, slots=True)
class AuthorDTO(DTO):
    name: str


@dataclass(frozen=True, slots=True)
class DetailedCVDTO(DTO):
    title: str
    is_visible: bool
    salary: SalaryDTO
    employment_types: list[EmploymentTypeDTO]
    work_schedules: list[WorkScheduleDTO]
    work_exp: list[WorkExpDTO]
    work_formats: list[WorkFormatDTO]
    skills: list[SkillDTO]
    education: EducationEnum
    email: str
    author: AuthorDTO

    additional_skills: list[SkillDTO] | None
    address: str | None
    about_me: str | None
    cv_file: str | None
    id: UUID


@dataclass(frozen=True, slots=True)
class CVDTO(DTO):
    title: str
    is_visible: bool
    salary: SalaryDTO
    skills: list[SkillDTO]
    author: AuthorDTO

    additional_skills: list[SkillDTO] | None
    about_me: str | None
    cv_file: str | None
    id: UUID
