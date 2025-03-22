from typing import TYPE_CHECKING, Protocol
from uuid import UUID

from application.articles.dto.article import ArticleDTO, PaginatedArticleDTO, TagDTO
from application.common.dto import PaginatedDTO

if TYPE_CHECKING:
    from application.articles.commands import CreateArticle, EditArticle
    from application.articles.queries import GetArticles, GetTagList


class ArticleRepo(Protocol):
    async def create_article(self, article: "CreateArticle") -> None: ...
    async def update_article(self, article: "EditArticle") -> None: ...
    async def delete_article(self, article_id: UUID) -> None: ...


class ArticleReader(Protocol):
    async def get_article_by_id(self, article_id: UUID) -> ArticleDTO: ...
    async def get_tag_list(self, query: "GetTagList") -> PaginatedDTO[TagDTO]: ...
    async def get_articles(self, query: "GetArticles") -> PaginatedArticleDTO: ...
