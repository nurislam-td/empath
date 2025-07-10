from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4

from common.application.command import Command
from common.application.uow import UnitOfWork
from job.common.domain.enums import EducationEnum
from job.employment.api.schemas import CreateCVSchema
from job.employment.infrastructure.repositories.cv import AlchemyCVRepo
from job.recruitment.application.exceptions import EmptyEmploymentTypesError, EmptySkillsError, EmptyWorkSchedulesError


@dataclass(frozen=True)
class Salary:
    from_: int
    to: int | None = None


@dataclass(frozen=True)
class WorkExp:
    company_name: str
    title: str
    description: str
    start_date: date
    is_relevant: bool
    end_date: date | None


@dataclass(frozen=True)
class Skill:
    name: str
    id: UUID = field(default_factory=uuid4)


@dataclass(frozen=True)
class CreateCV(Command[None]):
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

    additional_skills: list[Skill] | UnsetType = UNSET
    address: str | UnsetType = UNSET
    about_me: str | UnsetType = UNSET
    cv_file: str | UnsetType = UNSET
    id: UUID = field(default_factory=uuid4)


@dataclass(slots=True)
class CreateCVHandler:
    _repo: AlchemyCVRepo
    _uow: UnitOfWork

    async def __call__(self, command: CreateCVSchema) -> None:
        if not command.skills:
            raise EmptySkillsError
        if not command.employment_type_ids:
            raise EmptyEmploymentTypesError
        if not command.work_schedule_ids:
            raise EmptyWorkSchedulesError
        await self._repo.create_cv(command)
        await self._uow.commit()
