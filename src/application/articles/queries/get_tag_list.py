from dataclasses import dataclass

from application.articles.dto.article import TagDTO
from application.articles.ports.repo import ArticleReader
from application.common.dto import PaginatedDTO
from application.common.query import PaginationParams, Query, QueryHandler


@dataclass(frozen=True, slots=True)
class GetTagList(Query[PaginatedDTO[TagDTO]]):
    pagination: PaginationParams
    name: str | None = None


@dataclass(frozen=True, slots=True)
class GetTagListHandler(QueryHandler[GetTagList, PaginatedDTO[TagDTO]]):
    _reader: ArticleReader

    async def __call__(self, query: GetTagList) -> PaginatedDTO[TagDTO]:
        return await self._reader.get_tag_list(query)
