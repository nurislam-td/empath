from dataclasses import dataclass
from uuid import UUID

from articles.application.dto.article import CommentDTO, TagDTO
from articles.application.ports.repo import CommentReader
from common.application.dto import PaginatedDTO
from common.application.query import PaginationParams, Query, QueryHandler


@dataclass(frozen=True, slots=True)
class GetComments(Query[PaginatedDTO[TagDTO]]):
    pagination: PaginationParams
    article_id: UUID
    user_id: UUID


@dataclass(frozen=True, slots=True)
class GetCommentsHandler(QueryHandler[GetComments, PaginatedDTO[CommentDTO]]):
    _reader: CommentReader

    async def __call__(self, query: GetComments) -> PaginatedDTO[CommentDTO]:
        return await self._reader.get_article_comments(
            user_id=query.user_id,
            article_id=query.article_id,
            pagination=query.pagination,
        )
