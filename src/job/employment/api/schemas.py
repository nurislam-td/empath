from uuid import UUID, uuid4

from msgspec import UNSET, UnsetType, field

from common.api.schemas import BaseStruct
from job.common.api.schemas import SalarySchema, SkillSchema
from job.common.domain.enums import EducationEnum, WorkExpEnum, WorkFormatEnum


class GetVacanciesFilters(BaseStruct):
    salary_from: int | None = None
    salary_to: int | None = None
    work_exp: list[WorkExpEnum] | None = None
    education: list[EducationEnum] | None = None
    work_format: list[WorkFormatEnum] | None = None
    exclude_word: list[str] | None = None
    include_word: list[str] | None = None
    search: str | None = None


class WorkExpSchema(BaseStruct):
    company_name: str
    title: str
    description: str
    start_date: str
    is_relevant: bool
    end_date: str | None


class CreateCVSchema(BaseStruct):
    title: str
    is_visible: bool
    salary: SalarySchema
    employment_type_ids: list[UUID]
    work_schedule_ids: list[UUID]
    work_exp: list[WorkExpSchema]
    work_formats_id: list[UUID]
    skills: list[SkillSchema]
    education: EducationEnum
    email: str
    author_id: UUID

    additional_skills: list[SkillSchema] | UnsetType = UNSET
    address: str | UnsetType = UNSET
    about_me: str | UnsetType = UNSET
    cv_file: str | UnsetType = UNSET
    id: UUID = field(default_factory=uuid4)
