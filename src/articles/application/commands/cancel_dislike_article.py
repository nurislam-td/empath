from dataclasses import dataclass
from uuid import UUID

from articles.application.ports.repo import ArticleReader, ArticleRepo
from common.application.command import Command, CommandHandler
from common.application.uow import UnitOfWork
from users.application.ports.repo import UserReader, UserRepo


@dataclass(frozen=True, slots=True)
class CancelDislikeArticle(Command[None]):
    id: UUID
    user_id: UUID


@dataclass
class CancelDislikeArticleHandler(CommandHandler[CancelDislikeArticle, None]):
    _article_repo: ArticleRepo
    _article_reader: ArticleReader
    _user_repo: UserRepo
    _user_reader: UserReader
    _uow: UnitOfWork

    async def __call__(self, command: CancelDislikeArticle) -> None:
        article = await self._article_reader.get_article_by_id(command.id)
        await self._article_repo.cancel_dislike_article(article_id=command.id, user_id=command.user_id)
        user = await self._user_reader.get_user_by_id(article.author.id)
        await self._user_repo.update_user({"rating": user.rating + 1}, {"id": user.id})
        await self._uow.commit()
