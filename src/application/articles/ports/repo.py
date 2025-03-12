from typing import Protocol
from uuid import UUID

from application.articles.commands.create_article import CreateArticle
from application.articles.commands.edit_article import EditArticle
from application.articles.dto.article import ArticleDTO


class ArticleRepo(Protocol):
    async def create_article(self, article: CreateArticle) -> None: ...
    async def update_article(self, article: EditArticle) -> None: ...
    async def delete_article(self, article_id: UUID) -> None: ...


class ArticleReader(Protocol):
    async def get_article_by_id(self, article_id: UUID) -> ArticleDTO: ...
