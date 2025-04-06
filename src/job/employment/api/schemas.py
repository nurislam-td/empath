from datetime import date
from typing import Annotated
from uuid import UUID, uuid4

from litestar.dto import DTOConfig, MsgspecDTO
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
    start_date: date
    is_relevant: bool
    end_date: date | None


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


create_cv_dto = MsgspecDTO[
    Annotated[CreateCVSchema, DTOConfig(exclude={"id", "author_id"}, rename_fields={"salary.from_": "from"})]
]


class UpdateCVSchema(BaseStruct):
    title: str | UnsetType = UNSET
    is_visible: bool | UnsetType = UNSET
    salary: SalarySchema | UnsetType = UNSET
    employment_type_ids: list[UUID] | UnsetType = UNSET
    work_schedule_ids: list[UUID] | UnsetType = UNSET
    work_exp: list[WorkExpSchema] | UnsetType = UNSET
    work_formats_id: list[UUID] | UnsetType = UNSET
    skills: list[SkillSchema] | UnsetType = UNSET
    education: EducationEnum | UnsetType = UNSET
    email: str | UnsetType = UNSET

    additional_skills: list[SkillSchema] | UnsetType = UNSET
    address: str | UnsetType = UNSET
    about_me: str | UnsetType = UNSET
    cv_file: str | UnsetType = UNSET
