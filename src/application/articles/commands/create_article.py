from dataclasses import dataclass
from typing import Any, TypedDict
from uuid import UUID

from application.articles.ports.repo import ArticleRepo
from application.common.command import Command, CommandHandler
from application.common.uow import UnitOfWork
from domain.articles.entities import Article, SubArticle, Tag
from domain.articles.value_objects import ArticleTitle, TagName
from domain.common.exceptions import UnexpectedError


@dataclass(slots=True)
class CreateArticle(Command[None]):
    author_id: UUID
    title: str
    text: str
    imgs: list[str]
    sub_articles: list[dict[str, Any]]
    tags: list[dict[str, Any]]
    is_visible: bool


@dataclass
class CreateArticleHandler(CommandHandler[CreateArticle, None]):
    _article_repo: ArticleRepo
    _uow: UnitOfWork

    async def __call__(self, command: CreateArticle):
        try:
            sub_articles = [
                SubArticle(
                    title=ArticleTitle(i["title"]), text=i["text"], imgs=i["imgs"]
                )
                for i in command.sub_articles
            ]
            tags = [Tag(id=i["id"], name=TagName(i["name"])) for i in command.tags]
        except KeyError as e:
            # TODO log this
            raise UnexpectedError(f"KeyError: {e}") from e

        article = Article(
            title=ArticleTitle(command.title),
            text=command.text,
            author_id=command.author_id,
            imgs=command.imgs,
            is_visible=command.is_visible,
            tags=tags,
            sub_articles=sub_articles,
        )

        await self._article_repo.create_article(article)
        article.pull_events()
        await self._uow.commit()
