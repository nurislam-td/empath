from dataclasses import dataclass

from articles.application.dto.article import TagDTO
from articles.application.ports.repo import ArticleReader
from common.application.dto import PaginatedDTO
from common.application.query import PaginationParams, Query, QueryHandler


@dataclass(frozen=True, slots=True)
class GetTagList(Query[PaginatedDTO[TagDTO]]):
    pagination: PaginationParams
    name: str | None = None


@dataclass(frozen=True, slots=True)
class GetTagListHandler(QueryHandler[GetTagList, PaginatedDTO[TagDTO]]):
    _reader: ArticleReader

    async def __call__(self, query: GetTagList) -> PaginatedDTO[TagDTO]:
        return await self._reader.get_tag_list(query)
