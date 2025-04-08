from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from common.application.dto import DTO
from job.common.application.dto import EmploymentTypeDTO, SalaryDTO, SkillDTO, WorkFormatDTO, WorkScheduleDTO
from job.common.domain.enums import EducationEnum, VacancyResponseStatusEnum, WorkExpEnum


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
    skills: list[str]
    author: AuthorDTO

    additional_skills: list[str] | None
    about_me: str | None
    cv_file: str | None
    id: UUID


@dataclass(frozen=True, slots=True)
class VacancyResponseDTO(DTO):
    response_author: str
    cv_title: str
    cv_id: UUID
    vacancy_id: UUID
    created_at: datetime
    response_email: str
    status: VacancyResponseStatusEnum


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
    status: VacancyResponseStatusEnum | None
    education: EducationEnum
    id: UUID
