from dataclasses import dataclass
from uuid import UUID

from articles.application.ports.repo import ArticleReader, ArticleRepo
from common.application.command import Command, CommandHandler
from common.application.uow import UnitOfWork


@dataclass(frozen=True, slots=True)
class LikeArticle(Command[None]):
    id: UUID
    user_id: UUID


@dataclass
class LikeArticleHandler(CommandHandler[LikeArticle, None]):
    _article_repo: ArticleRepo
    _article_reader: ArticleReader
    _uow: UnitOfWork

    async def __call__(self, command: LikeArticle) -> None:
        await self._article_reader.get_article_by_id(command.id)
        await self._article_repo.like_article(article_id=command.id, user_id=command.user_id)
        await self._uow.commit()
