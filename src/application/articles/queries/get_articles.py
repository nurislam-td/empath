from dataclasses import dataclass

from application.articles.dto.article import PaginatedArticleDTO
from application.articles.ports.repo import ArticleReader
from application.common.query import PaginationParams, Query, QueryHandler


@dataclass(frozen=True, slots=True)
class GetArticles(Query[PaginatedArticleDTO]):
    pagination: PaginationParams


@dataclass(frozen=True, slots=True)
class GetArticlesHandler(QueryHandler[GetArticles, PaginatedArticleDTO]):
    _reader: ArticleReader

    async def __call__(self, query: GetArticles) -> PaginatedArticleDTO:
        return await self._reader.get_articles(query)
