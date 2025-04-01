from typing import Annotated
from uuid import UUID, uuid4

from litestar.dto import DTOConfig, MsgspecDTO
from msgspec import UNSET, UnsetType, field

from common.api.schemas import BaseStruct
from job.recruitment.domain.enums import EducationEnum, WorkExpEnum, WorkFormatEnum


class Salary(BaseStruct):
    from_: int = field(name="from")
    to: int = field(name="to")


class Skill(BaseStruct):
    name: str
    id: UUID = field(default_factory=uuid4)


class CreateVacancySchema(BaseStruct):
    title: str
    is_visible: bool
    salary: Salary
    employment_type_ids: list[UUID]
    work_schedule_ids: list[UUID]
    work_exp: WorkExpEnum
    work_format: WorkFormatEnum
    skills: list[Skill]
    responsibility: str
    requirements: str
    education: EducationEnum
    email: str
    author_id: UUID
    additional_description: str | UnsetType = UNSET
    additional_skills: list[Skill] | UnsetType = UNSET
    address: str | UnsetType = UNSET
    id: UUID = field(default_factory=uuid4)


class UpdateVacancySchema(BaseStruct):
    title: str | UnsetType = UNSET
    is_visible: bool | UnsetType = UNSET
    salary: Salary | UnsetType = UNSET
    employment_type_ids: list[UUID] | UnsetType = UNSET
    work_schedule_ids: list[UUID] | UnsetType = UNSET
    work_exp: WorkExpEnum | UnsetType = UNSET
    work_format: WorkFormatEnum | UnsetType = UNSET
    skills: list[Skill] | UnsetType = UNSET
    responsibility: str | UnsetType = UNSET
    requirements: str | UnsetType = UNSET
    education: EducationEnum | UnsetType = UNSET
    email: str | UnsetType = UNSET
    additional_description: str | UnsetType = UNSET
    additional_skills: list[Skill] | UnsetType = UNSET
    address: str | UnsetType = UNSET


create_vacancy_dto = MsgspecDTO[
    Annotated[CreateVacancySchema, DTOConfig(exclude={"id", "author_id"}, rename_fields={"salary.from_": "from"})]
]
