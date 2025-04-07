import uuid
from datetime import date

from sqlalchemy import BigInteger, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from common.infrastructure.models import TimedBaseModel
from job.common.domain.enums import EducationEnum, WorkExpEnum, WorkFormatEnum


class JobBase(TimedBaseModel):
    __abstract__ = True
    __table_args__ = {"schema": "job"}  # noqa: RUF012


class Vacancy(JobBase):
    __tablename__ = "vacancy"

    responsibility: Mapped[str]
    requirements: Mapped[str]

    title: Mapped[str]
    is_visible: Mapped[bool]
    salary_from: Mapped[int] = mapped_column(BigInteger)
    salary_to: Mapped[int | None] = mapped_column(BigInteger)

    work_exp: Mapped[WorkExpEnum]
    education: Mapped[EducationEnum]
    email: Mapped[str]

    additional_description: Mapped[str | None]
    address: Mapped[str | None]

    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("auth.user.id", ondelete="CASCADE"))


class Skill(JobBase):
    __tablename__ = "skill"

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)


class EmploymentType(JobBase):
    __tablename__ = "employment_type"
    name: Mapped[str]


class WorkSchedule(JobBase):
    __tablename__ = "work_schedule"
    name: Mapped[str]


class WorkFormat(JobBase):
    __tablename__ = "work_format"
    name: Mapped[WorkFormatEnum] = mapped_column(String(length=50))


class RelVacancyWorkFormat(JobBase):
    __tablename__ = "rel_vacancy_work_format"

    id: None = None  # type: ignore  # noqa: PGH003
    work_format_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("job.work_format.id", ondelete="CASCADE"),
        primary_key=True,
    )
    vacancy_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job.vacancy.id", ondelete="CASCADE"), primary_key=True)


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


class Recruiter(JobBase):
    __tablename__ = "recruiter"

    id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("auth.user.id", ondelete="CASCADE"), primary_key=True)

    company_name: Mapped[str]
    about_us: Mapped[str]
    email: Mapped[str]


# --------------------------------------------CV--------------------------------------------------------------
class CV(JobBase):
    __tablename__ = "cv"

    title: Mapped[str]  # position
    is_visible: Mapped[bool]
    salary_from: Mapped[int | None] = mapped_column(BigInteger)
    salary_to: Mapped[int | None] = mapped_column(BigInteger)

    education: Mapped[EducationEnum] = mapped_column(Enum(EducationEnum, native_enum=False, length=50))
    email: Mapped[str]

    about_me: Mapped[str | None]
    address: Mapped[str | None]

    cv_file: Mapped[str | None]

    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("auth.user.id", ondelete="CASCADE"))


class WorkExp(JobBase):
    __tablename__ = "work_exp"

    company_name: Mapped[str]
    title: Mapped[str]
    description: Mapped[str]
    start_date: Mapped[date]
    end_date: Mapped[date | None]
    is_relevant: Mapped[bool]
    cv_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("job.cv.id", ondelete="CASCADE"), primary_key=True)


class RelCVWorkFormat(JobBase):
    __tablename__ = "rel_cv_work_format"

    id: None = None  # type: ignore  # noqa: PGH003
    work_format_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("job.work_format.id", ondelete="CASCADE"),
        primary_key=True,
    )
    cv_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job.cv.id", ondelete="CASCADE"), primary_key=True)


class RelCVEmploymentType(JobBase):
    __tablename__ = "rel_cv_employment_type"

    id: None = None  # type: ignore  # noqa: PGH003
    employment_type_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("job.employment_type.id", ondelete="CASCADE"), primary_key=True
    )
    cv_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job.cv.id", ondelete="CASCADE"), primary_key=True)


class RelCVWorkSchedule(JobBase):
    __tablename__ = "rel_cv_work_schedule"

    id: None = None  # type: ignore  # noqa: PGH003
    work_schedule_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("job.work_schedule.id", ondelete="CASCADE"),
        primary_key=True,
    )
    cv_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job.cv.id", ondelete="CASCADE"), primary_key=True)


class RelCVSkill(JobBase):
    __tablename__ = "rel_cv_skill"

    id: None = None  # type: ignore  # noqa: PGH003
    skill_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job.skill.id", ondelete="CASCADE"), primary_key=True)
    cv_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job.cv.id", ondelete="CASCADE"), primary_key=True)


class RelCVAdditionalSkill(JobBase):
    __tablename__ = "rel_cv_additional_skill"

    id: None = None  # type: ignore  # noqa: PGH003
    skill_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job.skill.id", ondelete="CASCADE"), primary_key=True)
    cv_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job.cv.id", ondelete="CASCADE"), primary_key=True)


class RelCVVacancy(JobBase):
    __tablename__ = "rel_cv_vacancy"

    id: None = None  # type: ignore  # noqa: PGH003
    cv_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job.cv.id", ondelete="CASCADE"), primary_key=True)
    vacancy_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job.vacancy.id", ondelete="CASCADE"), primary_key=True)
