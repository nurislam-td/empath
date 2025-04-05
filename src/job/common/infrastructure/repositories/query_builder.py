from dataclasses import dataclass
from typing import TYPE_CHECKING, Any
from uuid import UUID

from sqlalchemy import Select, func, or_, select

from job.common.infrastructure.models import (
    EmploymentType,
    Recruiter,
    RelVacancyAdditionalSkill,
    RelVacancyEmploymentType,
    RelVacancySkill,
    RelVacancyWorkFormat,
    RelVacancyWorkSchedule,
    Skill,
    Vacancy,
    WorkFormat,
    WorkSchedule,
)

if TYPE_CHECKING:
    from job.common.application.queries.get_vacancies import GetVacanciesQuery

_vacancy = Vacancy
_recruiter = Recruiter
_skill = Skill
_schedule = WorkSchedule
_employment_type = EmploymentType
_work_format = WorkFormat
_rel_schedule_vacancy = RelVacancyWorkSchedule
_rel_employment_vacancy = RelVacancyEmploymentType
_rel_skill_vacancy = RelVacancySkill
_rel_additional_skill_vacancy = RelVacancyAdditionalSkill
_rel_work_format_vacancy = RelVacancyWorkFormat


@dataclass
class SkillFilters:
    include: list[str] | None = None
    exclude: list[str] | None = None


def filter_vacancy(qs: Select[Any], filters: "GetVacanciesQuery") -> Select[Any]:
    if filters.salary_from:
        qs = qs.where(_vacancy.salary_from >= filters.salary_from)
    if filters.salary_to:
        qs = qs.where(_vacancy.salary_to <= filters.salary_to)
    if filters.work_exp:
        qs = qs.where(_vacancy.work_exp.lower().in_(filters.work_exp))
    if filters.education:
        qs = qs.where(_vacancy.education.in_(filters.education))
    if filters.work_format:
        format_filter = select(_rel_work_format_vacancy.vacancy_id).join(
            _work_format.__table__,
            (_work_format.name.in_(filters.work_format) & _work_format.id == _rel_work_format_vacancy.work_format_id),
        )
        qs = qs.where(_vacancy.id.in_(format_filter))
    if filters.exclude_word:
        for word in filters.exclude_word:
            qs = qs.where(_vacancy.title.not_ilike(f"%{word}%"))
            qs = qs.where(_vacancy.responsibility.not_ilike(f"%{word}%"))
            qs = qs.where(_vacancy.requirements.not_ilike(f"%{word}%"))
    if filters.include_word:
        conditions = [
            _vacancy.title.ilike(f"%{word}%")
            | _vacancy.responsibility.ilike(f"%{word}%")
            | _vacancy.requirements.ilike(f"%{word}%")
            for word in filters.include_word
        ]
        qs = qs.where(or_(*conditions))
    if filters.author_id:
        qs = qs.where(_vacancy.author_id == filters.author_id)

    return qs


def filter_skill(qs: Select[Any], filters: SkillFilters) -> Select[Any]:
    if include := filters.include:
        qs = qs.where(func.lower(_skill.name).in_({word.lower() for word in include}))
    if exclude := filters.exclude:
        qs = qs.where(func.lower(_skill.name).not_in({word.lower() for word in exclude}))

    return qs


def search_skill(qs: Select[Any], search: str) -> Select[Any]:
    qs = qs.where(_skill.name.ilike(f"%{search}%"))
    return qs.order_by(
        func.similarity(func.lower(_skill.name), func.lower(search)).desc(),
    )


def get_skill_qs(filters: SkillFilters | None = None, search: str | None = None) -> Select[Any]:
    qs = select(_skill.__table__)
    if filters:
        qs = filter_skill(qs, filters)
    if search:
        qs = search_skill(qs, search)
    return qs


def get_vacancy_additional_skill_qs(
    vacancies_id: list[UUID],
) -> Select[Any]:
    return (
        get_skill_qs()
        .add_columns(_rel_additional_skill_vacancy.vacancy_id)
        .join(
            _rel_additional_skill_vacancy.__table__,
            (_rel_additional_skill_vacancy.skill_id == _skill.id)
            & _rel_additional_skill_vacancy.vacancy_id.in_(vacancies_id),
        )
    )


def get_vacancy_skill_qs(
    vacancy_ids: list[UUID],
) -> Select[Any]:
    return (
        get_skill_qs()
        .add_columns(_rel_skill_vacancy.vacancy_id)
        .join(
            _rel_skill_vacancy.__table__,
            (_rel_skill_vacancy.skill_id == _skill.id) & _rel_skill_vacancy.vacancy_id.in_(vacancy_ids),
        )
    )


def get_work_schedules_qs(vacancies_id: list[UUID] | None = None) -> Select[Any]:
    qs = select(_schedule.__table__)
    if vacancies_id:
        qs = qs.add_columns(
            _rel_schedule_vacancy.vacancy_id,
        ).join(
            _rel_schedule_vacancy.__table__,
            (_rel_schedule_vacancy.work_schedule_id == _schedule.id)
            & _rel_schedule_vacancy.vacancy_id.in_(vacancies_id),
        )
    return qs


def get_employment_type_qs(vacancies_id: list[UUID] | None = None) -> Select[Any]:
    qs = select(_employment_type.__table__)
    if vacancies_id:
        qs = qs.add_columns(_rel_employment_vacancy.vacancy_id).join(
            _rel_employment_vacancy.__table__,
            (_rel_employment_vacancy.employment_type_id == _employment_type.id)
            & _rel_employment_vacancy.vacancy_id.in_(vacancies_id),
        )
    return qs


def get_work_format_qs(vacancies_id: list[UUID] | None = None) -> Select[Any]:
    qs = select(_work_format.__table__)
    if vacancies_id:
        qs = qs.add_columns(_rel_work_format_vacancy.vacancy_id).join(
            _rel_work_format_vacancy.__table__,
            (_rel_work_format_vacancy.work_format_id == _work_format.id)
            & _rel_work_format_vacancy.vacancy_id.in_(vacancies_id),
        )
    return qs


def search_vacancy(qs: Select[Any], search: str) -> Select[Any]:
    if search == "":
        return qs
    search_table = _rel_skill_vacancy.__table__.join(_skill.__table__, _rel_skill_vacancy.skill_id == _skill.id)
    skill = select(_rel_skill_vacancy.vacancy_id).select_from(search_table).where(_skill.name.ilike(f"%{search}%"))
    additional_skill = select(_rel_additional_skill_vacancy.vacancy_id)
    additional_skill = additional_skill.select_from(
        _rel_additional_skill_vacancy.__table__.join(
            _skill.__table__,
            (_rel_additional_skill_vacancy.skill_id == _skill.id),
        ),
    ).where(_skill.name.ilike(f"%{search}%"))

    qs = qs.where(
        _vacancy.id.in_(skill)
        | _vacancy.id.in_(additional_skill)
        | _vacancy.title.ilike(f"%{search}%")
        | _vacancy.responsibility.ilike(f"%{search}%")
        | _vacancy.requirements.ilike(f"%{search}%")
        | _vacancy.additional_description.ilike(f"%{search}%"),
    )

    return qs.order_by(
        func.similarity(func.lower(_vacancy.title), func.lower(search)).desc(),
    )


def get_vacancy_qs(filters: "GetVacanciesQuery | None" = None, search: str | None = None) -> Select[Any]:
    table = _vacancy.__table__.outerjoin(_recruiter.__table__, _vacancy.author_id == _recruiter.id)
    qs = select(
        _vacancy.__table__,
        _recruiter.company_name.label("company_name"),
        _recruiter.about_us.label("about_company"),
        _recruiter.email.label("company_email"),
    ).select_from(table)
    if filters:
        qs = filter_vacancy(qs, filters)
    if search:
        qs = search_vacancy(qs, search)

    return qs
