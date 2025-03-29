from typing import TYPE_CHECKING, Protocol
from uuid import UUID

from articles.application.dto.article import ArticleDTO, CommentDTO, PaginatedArticleDTO, TagDTO
from common.application.dto import PaginatedDTO
from common.application.query import PaginationParams

if TYPE_CHECKING:
    from articles.application.commands import CreateArticle, CreateComment, EditArticle, EditComment
    from articles.application.queries import GetArticles, GetTagList


class ArticleRepo(Protocol):
    async def create_article(self, article: "CreateArticle") -> None: ...
    async def update_article(self, article: "EditArticle") -> None: ...
    async def delete_article(self, article_id: UUID) -> None: ...


class ArticleReader(Protocol):
    async def get_article_by_id(self, article_id: UUID) -> ArticleDTO: ...
    async def get_tag_list(self, query: "GetTagList") -> PaginatedDTO[TagDTO]: ...
    async def get_articles(self, query: "GetArticles") -> PaginatedArticleDTO: ...


class CommentRepo(Protocol):
    async def create_comment(self, comment: "CreateComment") -> None: ...
    async def update_comment(self, comment: "EditComment") -> None: ...
    async def delete_comment(self, comment_id: UUID) -> None: ...


class CommentReader(Protocol):
    async def get_article_comments(
        self,
        article_id: UUID,
        pagination: PaginationParams,
    ) -> PaginatedDTO[CommentDTO]: ...
    async def get_comment_by_id(self, comment_id: UUID) -> CommentDTO: ...
