import asyncio
from collections.abc import Coroutine, Iterable, Sequence
from typing import Any
from uuid import UUID

from sqlalchemy import Select, delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine.row import RowMapping

from articles.application.commands.create_article import CreateArticle
from articles.application.commands.edit_article import EditArticle
from articles.application.dto.article import (
    ArticleDTO,
    PaginatedArticleDTO,
    SubArticleDTO,
    SubArticleWithArticleIdDTO,
    TagDTO,
)
from articles.application.exceptions import ArticleIdNotExistError
from articles.application.ports.repo import ArticleReader, ArticleRepo
from articles.application.queries.get_articles import GetArticles
from articles.application.queries.get_tag_list import GetTagList
from articles.infrastructure.mapper import (
    convert_db_to_article_dto,
    convert_db_to_article_dto_list,
    convert_db_to_sub_article_dto_list,
    convert_db_to_tag_dto,
)
from articles.infrastructure.models import Article, ArticleImg, RelArticleTag, SubArticle, SubArticleImg, Tag
from articles.infrastructure.repositories.filters import TagFilters
from auth.infrastructure.models import User
from common.application.dto import PaginatedDTO
from common.domain.constants import Empty
from common.infrastructure.db.repositories.base import AlchemyReader, AlchemyRepo
from common.infrastructure.db.repositories.pagination import AlchemyPaginator


class AlchemyArticleRepo(AlchemyRepo, ArticleRepo):
    """Article Repo implementation."""

    article = Article
    sub_article = SubArticle
    sub_article_img = SubArticleImg
    article_img = ArticleImg
    tag = Tag
    rel_article_tag = RelArticleTag

    async def create_sub_article_imgs(self, sub_article_id: UUID, imgs: list[str]) -> None:
        await self.execute(
            insert(self.sub_article_img).values([{"sub_article_id": sub_article_id, "url": url} for url in imgs])
        )

    async def create_article_imgs(self, article_id: UUID, imgs: list[str]) -> None:
        await self.execute(insert(self.article_img).values([{"article_id": article_id, "url": url} for url in imgs]))

    async def create_sub_articles(self, article_id: UUID, sub_articles: list[SubArticleDTO]) -> None:
        if not sub_articles:
            return

        await self.execute(
            insert(self.sub_article).values(
                [
                    {"id": dto.id, "title": dto.title, "text": dto.text, "article_id": article_id}
                    for dto in sub_articles
                ],
            ),
        )

        await asyncio.gather(*(self.create_sub_article_imgs(dto.id, dto.imgs) for dto in sub_articles))

    async def create_tags_if_not_exists(self, tags: list[TagDTO]) -> None:
        await self.execute(
            insert(self.tag).values([tag.to_dict() for tag in tags]).on_conflict_do_nothing(),
        )

    async def map_tags_to_article(self, tag_ids: set[UUID], article_id: UUID) -> None:
        if not tag_ids:
            return
        await self.execute(
            insert(self.rel_article_tag).values([{"tag_id": tag_id, "article_id": article_id} for tag_id in tag_ids])
        )

    async def create_article(self, article: CreateArticle) -> None:
        await self.execute(
            insert(self.article).values(
                title=article.title,
                text=article.text,
                is_visible=article.is_visible,
                author_id=article.author_id,
                id=article.id,
            ),
        )
        tasks: list[Coroutine[Any, Any, Any]] = []
        if article.sub_articles:
            tasks.append(self.create_sub_articles(article.id, article.sub_articles))
        if article.imgs:
            tasks.append(self.create_article_imgs(article.id, article.imgs))

        await asyncio.gather(
            *tasks,
            self.create_tags_if_not_exists(article.tags),
            self.map_tags_to_article({dto.id for dto in article.tags}, article.id),
        )

    async def delete_article_imgs(self, article_id: UUID) -> None:
        await self.execute(delete(self.article_img).filter(self.article_img.article_id == article_id))

    async def delete_sub_articles(self, article_id: UUID) -> None:
        await self.execute(delete(self.sub_article).filter(self.sub_article.article_id == article_id))

    async def update_sub_articles(self, article_id: UUID, sub_articles: list[SubArticleDTO]) -> None:
        await self.delete_sub_articles(article_id)
        await self.create_sub_articles(article_id=article_id, sub_articles=sub_articles)

    async def unmap_tags_from_article(self, article_id: UUID) -> None:
        await self.execute(delete(self.rel_article_tag).filter(self.rel_article_tag.article_id == article_id))

    async def update_article_imgs(self, article_id: UUID, imgs: list[str]) -> None:
        await asyncio.gather(
            self.delete_article_imgs(article_id),
            self.create_article_imgs(article_id, imgs),
        )

    async def update_article_tags(self, article_id: UUID, tags: list[TagDTO]) -> None:
        await asyncio.gather(
            self.unmap_tags_from_article(article_id),
        )
        await self.create_tags_if_not_exists(tags)
        await self.map_tags_to_article({dto.id for dto in tags}, article_id)

    async def update_article(self, article: EditArticle) -> None:
        article_dict = article.to_dict_exclude_unset()
        article_id = article_dict.pop("id")
        article_dict.pop("author_id")
        article_dict.pop("sub_articles", None)
        article_dict.pop("imgs", None)
        article_dict.pop("tags", None)

        query = update(self.article).values(article_dict).filter(self.article.id == article_id)

        tasks: list[Coroutine[Any, Any, Any]] = []
        if article.sub_articles is not Empty.UNSET:
            tasks.append(self.update_sub_articles(article_id=article_id, sub_articles=article.sub_articles))

        if article.imgs is not Empty.UNSET:
            tasks.append(self.update_article_imgs(article_id, article.imgs))

        if article.tags is not Empty.UNSET:
            tasks.append(self.update_article_tags(article_id, article.tags))

        await asyncio.gather(*tasks, self.execute(query))

    async def delete_article(self, article_id: UUID) -> None:
        await self.execute(delete(self.article).where(self.article.id == article_id))


class AlchemyArticleReader(AlchemyReader, ArticleReader):
    """Article Reader implementation."""

    paginator = AlchemyPaginator
    article = Article
    sub_article = SubArticle
    sub_article_img = SubArticleImg
    article_img = ArticleImg
    tag = Tag
    rel_article_tag = RelArticleTag
    author = User

    async def get_sub_article_imgs(self, sub_article_ids: set[UUID]) -> Sequence[RowMapping]:
        return await self.fetch_all(
            select(self.sub_article_img.__table__).where(
                self.sub_article_img.sub_article_id.in_(sub_article_ids),
            ),
        )

    async def get_sub_articles(self, article_ids: Iterable[UUID] | None = None) -> list[SubArticleWithArticleIdDTO]:
        query = select(self.sub_article.__table__)

        if article_ids:
            query = query.where(self.sub_article.article_id.in_(article_ids))
        sub_articles = await self.fetch_all(query)
        sub_article_ids = {i.id for i in sub_articles}
        sub_article_imgs = await self.get_sub_article_imgs(sub_article_ids)

        return convert_db_to_sub_article_dto_list(sub_articles=sub_articles, sub_article_imgs=sub_article_imgs)

    def get_img_urls_qs(self, article_ids: set[UUID] | None = None) -> Select[Any]:
        query = select(self.article_img.url)
        if article_ids:
            query = query.where(self.article_img.article_id.in_(article_ids))
        return query

    def get_img_qs(self, article_ids: set[UUID] | None = None) -> Select[Any]:
        query = select(self.article_img.__table__)
        if article_ids:
            query = query.where(self.article_img.article_id.in_(article_ids))
        return query

    def get_tags_qs(self, article_ids: set[UUID] | None = None) -> Select[Any]:
        table = self.tag.__table__
        selected: list[Any] = [self.tag.__table__]

        if article_ids:
            selected.append(self.rel_article_tag.article_id)
            table = table.join(
                self.rel_article_tag.__table__,
                (self.tag.id == self.rel_article_tag.tag_id) & (self.rel_article_tag.article_id.in_(article_ids)),
            )

        return select(*selected).select_from(table)

    def get_articles_qs(self) -> Select[Any]:
        article_authors_join = self.article.__table__.join(
            self.author.__table__,
            self.article.author_id == self.author.id,
        )
        return select(
            self.article.__table__,
            self.author.nickname.label("author_nickname"),
            self.author.name.label("author_name"),
            self.author.lastname.label("author_lastname"),
            self.author.patronymic.label("author_patronymic"),
        ).select_from(article_authors_join)

    async def get_article_by_id(self, article_id: UUID) -> ArticleDTO:
        qs = self.get_articles_qs()
        qs = qs.where(self.article.id == article_id)
        article = await self.fetch_one(qs)
        if not article:
            raise ArticleIdNotExistError(article_id)
        sub_articles, article_imgs, article_tags = await asyncio.gather(
            self.get_sub_articles({article_id}),
            self.fetch_sequence(self.get_img_urls_qs({article_id})),
            self.fetch_all(self.get_tags_qs({article_id})),
        )
        return convert_db_to_article_dto(article, sub_articles, article_imgs, article_tags)

    async def get_articles(self, query: GetArticles) -> PaginatedArticleDTO:
        qs = self.get_articles_qs()

        value_count = await self.count(qs)
        qs = self.paginator.paginate(qs, query.pagination.page, query.pagination.per_page)
        page_count = self.paginator.get_page_count(value_count, query.pagination.per_page)

        articles = await self.fetch_all(qs)
        article_ids = {article.id for article in articles}
        sub_articles, article_imgs, article_tags = await asyncio.gather(
            self.get_sub_articles(article_ids),
            self.fetch_all(self.get_img_qs(article_ids)),
            self.fetch_all(self.get_tags_qs(article_ids)),
        )
        article_dto_list = convert_db_to_article_dto_list(
            articles=articles, sub_articles=sub_articles, imgs=article_imgs, tags=article_tags
        )

        return PaginatedDTO[ArticleDTO](count=page_count, page=query.pagination.page, results=article_dto_list)

    async def get_tag_list(self, query: GetTagList) -> PaginatedDTO[TagDTO]:
        qs = self.get_tags_qs()
        qs = TagFilters(name=query.name).filter_qs(qs).order_by(self.tag.name)

        paginated_query = self.paginator.paginate(
            query=qs, page=query.pagination.page, per_page=query.pagination.per_page
        )
        value_count = await self.count(qs)
        tags = await self.fetch_all(paginated_query)
        page_count = self.paginator.get_page_count(value_count, query.pagination.per_page)

        return PaginatedDTO[TagDTO](
            count=page_count, page=query.pagination.page, results=[convert_db_to_tag_dto(tag) for tag in tags]
        )
