from typing import NotRequired, Protocol, TypedDict, Unpack
from uuid import UUID

from msgspec import UNSET, UnsetType

from job.common.domain.enums import EducationEnum
from job.employment.application.commands.create_cv import Salary, Skill, WorkExp


class CVDataKwargs(TypedDict):
    title: NotRequired[str]
    is_visible: NotRequired[bool]
    salary: NotRequired[Salary]
    employment_type_ids: NotRequired[list[UUID]]
    work_schedule_ids: NotRequired[list[UUID]]
    work_exp: NotRequired[list[WorkExp]]
    work_formats_id: NotRequired[list[UUID]]
    skills: NotRequired[list[Skill]]
    education: NotRequired[EducationEnum]
    email: NotRequired[str]
    author_id: NotRequired[UUID]
    additional_skills: NotRequired[list[Skill] | UnsetType]
    address: NotRequired[str | UnsetType]
    about_me: NotRequired[str | UnsetType]
    cv_file: NotRequired[str | UnsetType]
    id: NotRequired[UUID]


class CVData(TypedDict):
    title: str
    is_visible: bool
    salary: Salary
    employment_type_ids: list[UUID]
    work_schedule_ids: list[UUID]
    work_exp: list[WorkExp]
    work_formats_id: list[UUID]
    skills: list[Skill]
    education: EducationEnum
    email: str
    author_id: UUID
    additional_skills: list[Skill] | UnsetType
    address: str | UnsetType
    about_me: str | UnsetType
    cv_file: str | UnsetType
    id: UUID


class CVDataFactory(Protocol):
    def __call__(
        self,
        **kwargs: Unpack[CVDataKwargs],
    ) -> CVData: ...
