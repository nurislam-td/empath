import math
from typing import Any

from sqlalchemy import Select


class AlchemyPaginator:
    @staticmethod
    def get_offset(current_page: int, per_page: int) -> int:
        return (current_page - 1) * per_page

    @classmethod
    def paginate(cls, query: Select[Any], page: int, per_page: int) -> Select[Any]:
        offset = cls.get_offset(page, per_page)
        return query.offset(offset).limit(per_page)

    @staticmethod
    def get_page_count(value_count: int, per_page: int) -> int:
        return math.ceil(value_count / per_page)
