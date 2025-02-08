from dataclasses import dataclass, field

from litestar.params import Parameter


@dataclass(frozen=True, slots=True)
class PaginationParams:
    page: int
    per_page: int = field(default=5)


async def pagination_query_params(
    page: int = Parameter(query="page"), per_page: int = Parameter(query="perPage")
) -> PaginationParams:
    return PaginationParams(page=page, per_page=per_page)
