from dataclasses import dataclass, field
from uuid import UUID, uuid4

from application.articles.dto.article import SubArticleDTO, TagDTO
from application.articles.mapper import (
    convert_strategy,
)
from application.articles.ports.repo import ArticleRepo
from application.common.command import Command, CommandHandler
from application.common.uow import UnitOfWork
from domain.articles.entities.article import Article
from domain.articles.events.article_created import ArticleCreated


@dataclass(slots=True, frozen=True)
class CreateArticle(Command[None]):
    title: str
    text: str
    author_id: UUID
    tags: list[TagDTO]
    is_visible: bool
    imgs: list[str] = field(default_factory=list)
    sub_articles: list[SubArticleDTO] = field(default_factory=list)
    views_cnt: int = 0
    likes_cnt: int = 0
    dislikes_cnt: int = 0
    id: UUID = field(default_factory=uuid4)


@dataclass
class CreateArticleHandler(CommandHandler[CreateArticle, None]):
    _article_repo: ArticleRepo
    _uow: UnitOfWork

    async def __call__(self, command: CreateArticle) -> None:
        converted_data = {
            attr: convert_strategy.get(attr, lambda x: x)(value) for attr, value in command.to_dict().items()
        }
        article = Article(**converted_data)
        article.record_event(ArticleCreated(author_id=article.author_id, article_id=article.id))
        await self._article_repo.create_article(command)
        article.pull_events()
        await self._uow.commit()
