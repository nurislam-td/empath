from dataclasses import dataclass
from itertools import chain
from uuid import UUID

from articles.application.dto.article import SubArticleDTO, TagDTO
from articles.application.exceptions import EmptyArticleUpdatesError
from articles.application.mapper import (
    convert_dto_to_article,
    convert_strategy,
)
from articles.application.ports.repo import ArticleReader, ArticleRepo
from articles.domain.entities.article import EmptyTagListError
from common.application.command import Command, CommandHandler
from common.application.ports.file_storage import FileStorage
from common.application.uow import UnitOfWork
from common.domain.constants import Empty


@dataclass(frozen=True, slots=True)
class EditArticle(Command[None]):
    id: UUID
    author_id: UUID
    title: str = Empty.UNSET
    text: str = Empty.UNSET
    tags: list[TagDTO] | Empty = Empty.UNSET
    is_visible: bool | Empty = Empty.UNSET
    imgs: list[str] | Empty = Empty.UNSET
    sub_articles: list[SubArticleDTO] | Empty = Empty.UNSET


@dataclass
class EditArticleHandler(CommandHandler[EditArticle, None]):
    _article_repo: ArticleRepo
    _article_reader: ArticleReader
    _file_manager: FileStorage
    _uow: UnitOfWork

    async def __call__(self, command: EditArticle) -> None:
        article_dto = await self._article_reader.get_article_by_id(command.id)
        article = convert_dto_to_article(article_dto)
        if len(keys := command.to_dict_exclude_unset().keys()) == 2 and {"author_id", "id"} <= keys:  # noqa: PLR2004
            raise EmptyArticleUpdatesError

        for attr, value in command.to_dict_exclude_unset().items():
            convert_fun = convert_strategy.get(attr, lambda x: x)
            setattr(article, attr, convert_fun(value))
        if not article.tags:
            raise EmptyTagListError

        await self._article_repo.update_article(command)
        await self._uow.commit()

        if command.imgs is not Empty.UNSET and (imgs := set(article_dto.imgs)):
            img_for_delete = imgs - set(command.imgs)
            await self._file_manager.delete_files(img_for_delete)

        if command.sub_articles is not Empty.UNSET and (
            sub_imgs := set(chain.from_iterable(sub_article.imgs for sub_article in article_dto.sub_articles))
        ):
            img_for_delete = sub_imgs - set(
                chain.from_iterable(sub_article.imgs for sub_article in command.sub_articles)
            )
            await self._file_manager.delete_files(img_for_delete)
