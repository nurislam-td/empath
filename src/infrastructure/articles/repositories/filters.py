from dataclasses import dataclass
from typing import Any

from sqlalchemy import Select, func

from infrastructure.articles.models import Tag


@dataclass
class TagFilters:
    name: str | None = None

    def filter_qs(self, qs: Select[Any]) -> Select[Any]:
        if self.name:
            qs = qs.order_by(func.similarity(Tag.name, self.name).desc())
        return qs
