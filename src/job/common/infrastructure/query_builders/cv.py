from typing import Any
from uuid import UUID

from sqlalchemy import Select, select

from auth.infrastructure.models import User
from job.common.infrastructure.models import (
    CV,
    EmploymentType,
    RelCVAdditionalSkill,
    RelCVEmploymentType,
    RelCVSkill,
    RelCVWorkFormat,
    RelCVWorkSchedule,
    Skill,
    WorkExp,
    WorkFormat,
    WorkSchedule,
)
from job.common.infrastructure.query_builders.common import (
    get_skill_qs,
)

_cv = CV
_cv_author = User
_rel_cv_skill = RelCVSkill
_rel_cv_schedule = RelCVWorkSchedule
_rel_cv_employment_type = RelCVEmploymentType
_rel_cv_work_format = RelCVWorkFormat
_rel_cv_additional_skill = RelCVAdditionalSkill

_work_exp = WorkExp
_skill = Skill
_schedule = WorkSchedule
_employment_type = EmploymentType
_work_format = WorkFormat


def get_cv_qs() -> Select[Any]:
    table = _cv.__table__.join(_cv_author.__table__, _cv.author_id == _cv_author.id)
    qs = select(
        _cv.__table__,
        _cv_author.name.label("author_name"),
        _cv_author.lastname.label("author_lastname"),
        _cv_author.patronymic.label("author_patronymic"),
    ).select_from(table)

    return qs


def get_cv_additional_skill_qs(
    cv_ids: list[UUID],
) -> Select[Any]:
    return (
        get_skill_qs()
        .add_columns(_rel_cv_additional_skill.cv_id)
        .join(
            _rel_cv_additional_skill.__table__,
            (_rel_cv_additional_skill.skill_id == _skill.id) & _rel_cv_additional_skill.cv_id.in_(cv_ids),
        )
    )


def get_cv_skill_qs(
    cv_ids: list[UUID],
) -> Select[Any]:
    return (
        get_skill_qs()
        .add_columns(_rel_cv_skill.cv_id)
        .join(
            _rel_cv_skill.__table__,
            (_rel_cv_skill.skill_id == _skill.id) & _rel_cv_skill.cv_id.in_(cv_ids),
        )
    )


def get_cv_work_schedules_qs(cv_ids: list[UUID]) -> Select[Any]:
    qs = select(_schedule.__table__)
    if cv_ids:
        qs = qs.add_columns(
            _rel_cv_schedule.cv_id,
        ).join(
            _rel_cv_schedule.__table__,
            (_rel_cv_schedule.work_schedule_id == _schedule.id) & _rel_cv_schedule.cv_id.in_(cv_ids),
        )
    return qs


def get_cv_employment_type_qs(cv_ids: list[UUID]) -> Select[Any]:
    qs = select(_employment_type.__table__)
    if cv_ids:
        qs = qs.add_columns(_rel_cv_employment_type.cv_id).join(
            _rel_cv_employment_type.__table__,
            (_rel_cv_employment_type.employment_type_id == _employment_type.id)
            & _rel_cv_employment_type.cv_id.in_(cv_ids),
        )
    return qs


def get_cv_work_format_qs(cv_ids: list[UUID]) -> Select[Any]:
    qs = select(_work_format.__table__)
    if cv_ids:
        qs = qs.add_columns(_rel_cv_work_format.cv_id).join(
            _rel_cv_work_format.__table__,
            (_rel_cv_work_format.work_format_id == _work_format.id) & _rel_cv_work_format.cv_id.in_(cv_ids),
        )
    return qs


def get_cv_work_exp_qs(cv_ids: list[UUID]) -> Select[Any]:
    qs = select(_work_exp.__table__)
    if cv_ids:
        qs = qs.where(
            _work_exp.cv_id.in_(cv_ids),
        )
    return qs
