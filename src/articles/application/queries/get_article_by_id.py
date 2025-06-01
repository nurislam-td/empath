from dataclasses import dataclass
from uuid import UUID

from articles.application.dto.article import ArticleDTO
from articles.application.ports.repo import ArticleReader
from common.application.query import Query, QueryHandler


@dataclass(frozen=True, slots=True)
class GetArticleById(Query[ArticleDTO]):
    article_id: UUID
    user_id: UUID


@dataclass(frozen=True, slots=True)
class GetArticleByIdHandler(QueryHandler[GetArticleById, ArticleDTO]):
    _reader: ArticleReader

    async def __call__(self, query: GetArticleById) -> ArticleDTO:
        return await self._reader.get_article_by_id(user_id=query.user_id, article_id=query.article_id)
