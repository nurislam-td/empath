from typing import TYPE_CHECKING, Any
from uuid import UUID

from sqlalchemy import Select, func, or_, select

from auth.infrastructure.models import User
from job.common.infrastructure.models import (
    CV,
    RelCVVacancy,
    Vacancy,
)

if TYPE_CHECKING:
    from job.common.application.queries.get_vacancy_responses import GetVacancyResponsesQuery

_vacancy = Vacancy
_cv = CV
_cv_author = User
_rel_cv_vacancy = RelCVVacancy


def filter_vacancy_response(qs: Select[Any], filters: "GetVacancyResponsesQuery") -> Select[Any]:
    if filters.vacancy_id:
        qs = qs.where(_rel_cv_vacancy.vacancy_id == filters.vacancy_id)
    if filters.response_author_id:
        qs = qs.where(_cv_author.id == filters.response_author_id)
    if filters.vacancy_author_id:
        qs = qs.where(_vacancy.author_id == filters.vacancy_author_id)
    return qs


def get_vacancy_responses_qs(filters: "GetVacancyResponsesQuery | None" = None) -> Select[Any]:
    table = (
        _rel_cv_vacancy.__table__.join(_cv.__table__, _rel_cv_vacancy.cv_id == _cv.id)
        .join(_vacancy.__table__, _rel_cv_vacancy.vacancy_id == _vacancy.id)
        .join(_cv_author.__table__, _cv.author_id == _cv_author.id)
    )
    qs = select(
        _cv_author.name.label("author_name"),
        _cv_author.lastname.label("author_lastname"),
        _cv_author.patronymic.label("author_patronymic"),
        _cv.title.label("cv_title"),
        _cv.id.label("cv_id"),
        _vacancy.id.label("vacancy_id"),
        _rel_cv_vacancy.created_at,
        _cv_author.email.label("response_email"),
        _rel_cv_vacancy.status,
    ).select_from(table)
    if filters:
        qs = filter_vacancy_response(qs, filters)
    return qs
