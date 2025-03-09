from dataclasses import dataclass

from application.articles.dto.article import ArticleDTO
from application.articles.mapper import (
    convert_dto_to_article,
)
from application.articles.ports.repo import ArticleRepo
from application.common.command import Command, CommandHandler
from application.common.uow import UnitOfWork


@dataclass(slots=True, frozen=True)
class CreateArticle(Command[None], ArticleDTO):
    pass


@dataclass
class CreateArticleHandler(CommandHandler[CreateArticle, None]):
    _article_repo: ArticleRepo
    _uow: UnitOfWork

    async def __call__(self, command: CreateArticle) -> None:
        article = convert_dto_to_article(command)
        await self._article_repo.create_article(command)
        article.pull_events()
        await self._uow.commit()
