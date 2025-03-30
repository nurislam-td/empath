from litestar.params import Parameter

from common.application.query import PaginationParams


async def pagination_query_params(
    page: int = Parameter(query="page"), per_page: int = Parameter(query="per_page")
) -> PaginationParams:
    return PaginationParams(page=page, per_page=per_page)
