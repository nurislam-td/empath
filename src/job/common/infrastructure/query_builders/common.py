from dataclasses import dataclass
from typing import Any

from sqlalchemy import Select, func, select

from job.common.infrastructure.models import Skill

_skill = Skill


@dataclass
class SkillFilters:
    include: list[str] | None = None
    exclude: list[str] | None = None


def search_skill(qs: Select[Any], search: str) -> Select[Any]:
    qs = qs.where(_skill.name.ilike(f"%{search}%"))
    return qs.order_by(
        func.similarity(func.lower(_skill.name), func.lower(search)).desc(),
    )


def filter_skill(qs: Select[Any], filters: SkillFilters) -> Select[Any]:
    if include := filters.include:
        qs = qs.where(func.lower(_skill.name).in_({word.lower() for word in include}))
    if exclude := filters.exclude:
        qs = qs.where(func.lower(_skill.name).not_in({word.lower() for word in exclude}))

    return qs


def get_skill_qs(filters: SkillFilters | None = None, search: str | None = None) -> Select[Any]:
    qs = select(_skill.__table__)
    if filters:
        qs = filter_skill(qs, filters)
    if search:
        qs = search_skill(qs, search)
    return qs
