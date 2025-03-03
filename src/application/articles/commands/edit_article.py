from dataclasses import dataclass
from typing import Any
from uuid import UUID

from application.articles.ports.repo import ArticleRepo
from application.common.command import Command, CommandHandler
from application.common.uow import UnitOfWork


@dataclass
class EditArticle(Command[None]):
    title: str
    text: str
    author_id: UUID
    tags: list[str]
    is_visible: bool
    imgs: list[str]
    sub_articles: list[dict[str, Any]]


@dataclass
class UpdateAvatarHandler(CommandHandler[EditArticle, None]):
    _article_repo: ArticleRepo
    _uow: UnitOfWork

    async def __call__(self, command: EditArticle) -> None:
        await self._article_repo.update_article(command)
        await self._uow.commit()
