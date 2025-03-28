from dataclasses import dataclass
from uuid import UUID

from articles.application.ports.repo import ArticleRepo
from common.application.command import Command, CommandHandler
from common.application.uow import UnitOfWork


@dataclass(slots=True, frozen=True)
class DeleteArticle(Command[None]):
    article_id: UUID


@dataclass(slots=True, frozen=True)
class DeleteArticleHandler(CommandHandler[DeleteArticle, None]):
    _article_repo: ArticleRepo
    _uow: UnitOfWork

    async def __call__(self, command: DeleteArticle) -> None:
        await self._article_repo.delete_article(command.article_id)
        await self._uow.commit()
