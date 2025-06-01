from dataclasses import dataclass
from uuid import UUID

from articles.application.exceptions import NothingToCancelError
from articles.application.ports.repo import ArticleReader, ArticleRepo
from common.application.command import Command, CommandHandler
from common.application.uow import UnitOfWork
from users.application.ports.repo import UserReader, UserRepo


@dataclass(frozen=True, slots=True)
class DislikeArticle(Command[None]):
    id: UUID
    user_id: UUID


@dataclass
class DislikeArticleHandler(CommandHandler[DislikeArticle, None]):
    _article_repo: ArticleRepo
    _article_reader: ArticleReader
    _user_reader: UserReader
    _user_repo: UserRepo
    _uow: UnitOfWork

    async def __call__(self, command: DislikeArticle) -> None:
        article = await self._article_reader.get_article_by_id(user_id=command.user_id, article_id=command.id)
        minus_rating = 1

        try:
            await self._article_repo.cancel_like_article(article_id=command.id, user_id=command.user_id)
        except NothingToCancelError:
            pass
        else:
            minus_rating += 1

        await self._article_repo.dislike_article(article_id=command.id, user_id=command.user_id)
        user = await self._user_reader.get_user_by_id(article.author.id)
        await self._user_repo.update_user({"rating": user.rating - minus_rating}, {"id": user.id})
        await self._uow.commit()
