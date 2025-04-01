import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from common.infrastructure.models import TimedBaseModel
from job.recruitment.domain.enums import EducationEnum, WorkExpEnum, WorkFormatEnum


class JobBase(TimedBaseModel):
    __abstract__ = True
    __table_args__ = {"schema": "job"}  # noqa: RUF012


class Vacancy(JobBase):
    __tablename__ = "vacancy"

    responsibility: Mapped[str]
    requirements: Mapped[str]

    title: Mapped[str]
    is_visible: Mapped[bool]
    salary_from: Mapped[int]
    salary_to: Mapped[int | None]

    work_exp: Mapped[WorkExpEnum]
    work_format: Mapped[WorkFormatEnum]
    education: Mapped[EducationEnum]
    email: Mapped[str]

    additional_description: Mapped[str | None]
    address: Mapped[str | None]

    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("auth.user.id", ondelete="CASCADE"))


class Skill(JobBase):
    __tablename__ = "skill"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    responsibility: Mapped[str] = mapped_column(String, nullable=False)
    requirement: Mapped[str] = mapped_column(String, nullable=False)


class EmploymentType(JobBase):
    __tablename__ = "employment_type"
    name: Mapped[str]


class WorkSchedule(JobBase):
    __tablename__ = "work_schedule"
    name: Mapped[str]


class RelVacancyEmploymentType(JobBase):
    __tablename__ = "rel_vacancy_employment_type"

    id: None = None  # type: ignore  # noqa: PGH003
    employment_type_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("job.employment_type.id", ondelete="CASCADE"), primary_key=True
    )
    vacancy_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job.vacancy.id", ondelete="CASCADE"), primary_key=True)


class RelVacancyWorkSchedule(JobBase):
    __tablename__ = "rel_vacancy_work_schedule"

    id: None = None  # type: ignore  # noqa: PGH003
    work_schedule_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("job.work_schedule.id", ondelete="CASCADE"),
        primary_key=True,
    )
    vacancy_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job.vacancy.id", ondelete="CASCADE"), primary_key=True)


class RelVacancySkill(JobBase):
    __tablename__ = "rel_vacancy_skill"

    id: None = None  # type: ignore  # noqa: PGH003
    skill_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job.skill.id", ondelete="CASCADE"), primary_key=True)
    vacancy_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job.vacancy.id", ondelete="CASCADE"), primary_key=True)


class RelVacancyAdditionalSkill(JobBase):
    __tablename__ = "rel_vacancy_additional_skill"

    id: None = None  # type: ignore  # noqa: PGH003
    skill_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job.skill.id", ondelete="CASCADE"), primary_key=True)
    vacancy_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job.vacancy.id", ondelete="CASCADE"), primary_key=True)
