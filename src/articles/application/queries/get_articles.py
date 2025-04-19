from dataclasses import dataclass
from uuid import UUID

from articles.application.dto.article import PaginatedArticleDTO
from articles.application.ports.repo import ArticleReader
from common.application.dto import DTO
from common.application.query import PaginationParams, Query, QueryHandler


@dataclass(frozen=True, slots=True)
class ArticleFilter(DTO):
    search: str | None = None
    liked_user_id: UUID | None = None
    disliked_user_id: UUID | None = None
    viewed_user_id: UUID | None = None
    specializations_id: list[UUID] | None = None
    exclude_words: list[str] | None = None
    include_words: list[str] | None = None
    tags_id: list[UUID] | None = None


@dataclass(frozen=True, slots=True)
class GetArticles(Query[PaginatedArticleDTO]):
    pagination: PaginationParams
    articles_filter: ArticleFilter | None = None


@dataclass(frozen=True, slots=True)
class GetArticlesHandler(QueryHandler[GetArticles, PaginatedArticleDTO]):
    _reader: ArticleReader

    async def __call__(self, query: GetArticles) -> PaginatedArticleDTO:
        return await self._reader.get_articles(query)
