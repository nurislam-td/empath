import asyncio
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, ClassVar
from uuid import UUID

from sqlalchemy import Select, delete, select, update
from sqlalchemy.dialects.postgresql import insert

from articles.application.commands.create_article import CreateArticle
from articles.application.commands.edit_article import EditArticle
from articles.application.dto.article import (
    ArticleDTO,
    PaginatedArticleDTO,
)
from articles.application.exceptions import ArticleIdNotExistError
from articles.application.ports.repo import ArticleReader, ArticleRepo
from articles.application.queries.get_articles import GetArticles
from articles.infrastructure.mapper import (
    convert_db_to_article_dto,
    convert_db_to_article_dto_list,
)
from articles.infrastructure.models import Article, ArticleImg
from articles.infrastructure.repositories.comment import AlchemyCommentRepo
from articles.infrastructure.repositories.filters import ArticleQueryBuilder
from articles.infrastructure.repositories.sub_article import AlchemySubArticleReader, AlchemySubArticleRepo
from articles.infrastructure.repositories.tag import AlchemyTagReader, AlchemyTagRepo
from auth.infrastructure.models import User
from common.application.dto import PaginatedDTO
from common.domain.constants import Empty
from common.infrastructure.repositories.base import AlchemyReader, AlchemyRepo
from common.infrastructure.repositories.pagination import AlchemyPaginator

if TYPE_CHECKING:
    from collections.abc import Coroutine


@dataclass(slots=True)
class AlchemyArticleRepo(ArticleRepo):
    """Article Repo implementation."""

    _article: ClassVar[type[Article]] = Article
    _article_img: ClassVar[type[ArticleImg]] = ArticleImg

    _base: AlchemyRepo
    _sub_article: AlchemySubArticleRepo
    _tag: AlchemyTagRepo

    async def _create_article_imgs(self, article_id: UUID, imgs: list[str]) -> None:
        if not imgs:
            return
        await self._base.execute(
            insert(self._article_img).values([{"article_id": article_id, "url": url} for url in imgs])
        )

    async def create_article(self, article: CreateArticle) -> None:
        await self._base.execute(
            insert(self._article).values(
                title=article.title,
                text=article.text,
                is_visible=article.is_visible,
                author_id=article.author_id,
                id=article.id,
            ),
        )
        tasks: list[Coroutine[Any, Any, Any]] = []
        if article.sub_articles:
            tasks.append(self._sub_article.create_sub_articles(article.id, article.sub_articles))
        if article.imgs:
            tasks.append(self._create_article_imgs(article.id, article.imgs))

        await asyncio.gather(
            *tasks,
            self._tag.create_tags_if_not_exists(article.tags),
            self._tag.map_tags_to_article({dto.id for dto in article.tags}, article.id),
        )

    async def _delete_article_imgs(self, article_id: UUID) -> None:
        await self._base.execute(delete(self._article_img).filter(self._article_img.article_id == article_id))

    async def update_article_imgs(self, article_id: UUID, imgs: list[str]) -> None:
        await asyncio.gather(
            self._delete_article_imgs(article_id),
            self._create_article_imgs(article_id, imgs),
        )

    async def update_article(self, article: EditArticle) -> None:
        article_dict = article.to_dict_exclude_unset()
        article_id = article_dict.pop("id")
        article_dict.pop("author_id")
        article_dict.pop("sub_articles", None)
        article_dict.pop("imgs", None)
        article_dict.pop("tags", None)

        query = update(self._article).values(article_dict).filter(self._article.id == article_id)

        tasks: list[Coroutine[Any, Any, None]] = []
        if article.sub_articles is not Empty.UNSET:
            tasks.append(
                self._sub_article.update_sub_articles(article_id=article_id, sub_articles=article.sub_articles),
            )

        if article.imgs is not Empty.UNSET:
            tasks.append(self.update_article_imgs(article_id, article.imgs))

        if article.tags is not Empty.UNSET:
            tasks.append(self._tag.update_article_tags(article_id, article.tags))

        await asyncio.gather(*tasks, self._base.execute(query))

    async def delete_article(self, article_id: UUID) -> None:
        await self._base.execute(delete(self._article).where(self._article.id == article_id))


class AlchemyArticleReader(ArticleReader):
    """Article Reader implementation."""

    _paginator = AlchemyPaginator
    _article = Article
    _article_img = ArticleImg
    _author = User
    _qb = ArticleQueryBuilder

    def __init__(self, base: AlchemyReader, tag: AlchemyTagReader, sub_article: AlchemySubArticleReader) -> None:
        self._base = base
        self._sub_article = sub_article
        self._tag = tag

    async def get_article_by_id(self, article_id: UUID) -> ArticleDTO:
        qs = self._qb.get_articles_qs()
        qs = qs.where(self._article.id == article_id)
        article = await self._base.fetch_one(qs)
        if not article:
            raise ArticleIdNotExistError(article_id)
        sub_articles, article_imgs, article_tags = await asyncio.gather(
            self._sub_article.get_sub_articles({article_id}),
            self._base.fetch_sequence(self._qb.get_img_urls_qs({article_id})),
            self._base.fetch_all(self._tag.get_tags_qs({article_id})),
        )
        return convert_db_to_article_dto(article, sub_articles, article_imgs, article_tags)

    async def get_articles(self, query: GetArticles) -> PaginatedArticleDTO:
        qs = self._qb.get_articles_qs(article_filter=query.articles_filter)

        value_count = await self._base.count(qs)
        qs = self._paginator.paginate(qs, query.pagination.page, query.pagination.per_page)
        page_count = self._paginator.get_page_count(value_count, query.pagination.per_page)

        articles = await self._base.fetch_all(qs)
        article_ids = {article.id for article in articles}
        sub_articles, article_imgs, article_tags = await asyncio.gather(
            self._sub_article.get_sub_articles(article_ids),
            self._base.fetch_all(self._qb.get_img_qs(article_ids)),
            self._base.fetch_all(self._tag.get_tags_qs(article_ids)),
        )
        article_dto_list = convert_db_to_article_dto_list(
            articles=articles, sub_articles=sub_articles, imgs=article_imgs, tags=article_tags
        )

        return PaginatedDTO[ArticleDTO](count=page_count, page=query.pagination.page, results=article_dto_list)
