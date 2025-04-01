from typing import Any

from sqlalchemy import Select

from job.common.infrastructure.models import Vacancy

_vacancy = Vacancy


def filter_vacancy(qs: Select[Any]) -> Select[Any]:
    return qs
