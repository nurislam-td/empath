from typing import Any, Protocol
from uuid import UUID

from application.articles.commands.edit_article import EditArticle
from domain.articles import entities


class ArticleRepo(Protocol):
    async def create_article(
        self, article: entities.Article
    ) -> None: ...  # TODO implement

    async def update_article(self, command: EditArticle): ...
    async def delete_article(self, article_id: UUID): ...
