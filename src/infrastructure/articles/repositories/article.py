import asyncio
from collections import defaultdict
from collections.abc import Iterable
from typing import Any, Coroutine, Sequence
from uuid import UUID

from sqlalchemy import RowMapping, Select, delete, select, update
from sqlalchemy.dialects.postgresql import insert

from application.articles.commands.create_article import CreateArticle
from application.articles.commands.edit_article import EditArticle
from application.articles.dto.article import ArticleDTO, SubArticleDTO, TagDTO
from application.articles.exceptions import ArticleIdNotExistError
from application.articles.ports.repo import ArticleReader, ArticleRepo
from application.articles.queries.get_tag_list import GetTagList
from application.common.dto import PaginatedDTO
from infrastructure.articles.mapper import (
    convert_db_to_article_dto,
    convert_db_to_sub_article_dto,
    convert_db_to_tag_dto,
)
from infrastructure.articles.models import Article, ArticleImg, RelArticleTag, SubArticle, SubArticleImg, Tag
from infrastructure.articles.repositories.filters import TagFilters
from infrastructure.auth.models import User
from infrastructure.db.repositories.base import AlchemyReader, AlchemyRepo
from infrastructure.db.repositories.paginators import AlchemyPaginator


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

    async def map_tags_to_article(self, tag_ids: Iterable[UUID], article_id: UUID) -> None:
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

    async def delete_sub_article_imgs(self, sub_article_ids: Iterable[UUID]) -> None:
        await self.execute(
            delete(self.sub_article_img).filter(self.sub_article_img.sub_article_id.in_(sub_article_ids)),
        )

    async def delete_article_imgs(self, article_id: UUID) -> None:
        await self.execute(delete(self.article_img).filter(self.article_img.article_id == article_id))

    async def update_sub_articles(self, article_id: UUID, sub_articles: list[SubArticleDTO]) -> None:
        query = insert(self.sub_article).values(
            [{"title": dto.title, "text": dto.text, "article_id": article_id} for dto in sub_articles],
        )
        await self.execute(
            query.on_conflict_do_update(
                index_elements=["id"],
                set_={"title": query.excluded.title, "text": query.excluded.text},
            ),
        )
        await asyncio.gather(
            *(self.create_sub_article_imgs(dto.id, dto.imgs) for dto in sub_articles),
            self.delete_sub_article_imgs({dto.id for dto in sub_articles}),
        )

    async def delete_article_tags(self, article_id: UUID) -> None:
        await self.execute(delete(self.rel_article_tag).filter(self.rel_article_tag.article_id == article_id))

    async def update_article_imgs(self, article_id: UUID, imgs: list[str]) -> None:
        await asyncio.gather(
            self.delete_article_imgs(article_id),
            self.create_article_imgs(article_id, imgs),
        )

    async def update_article_tags(self, article_id: UUID, tags: list[TagDTO]) -> None:
        await asyncio.gather(
            self.delete_article_tags(article_id),
            self.create_tags_if_not_exists(tags),
            self.map_tags_to_article({dto.id for dto in tags}, article_id),
        )

    async def update_article(self, article: EditArticle) -> None:
        article_dict = article.to_dict_exclude_unset()
        article_id = article_dict.pop("id")
        article_dict.pop("author_id")
        sub_articles = article_dict.pop("sub_articles", None)
        imgs = article_dict.pop("imgs", None)
        tags = article_dict.pop("tags", None)

        query = update(self.article).values(article_dict).filter(self.article.id == article_id)

        tasks = []
        if sub_articles:
            tasks.append(self.update_sub_articles(article_id, sub_articles))

        if imgs:
            tasks.append(self.update_article_imgs(article_id, imgs))

        if tags:
            tasks.append(self.update_article_tags(article_id, tags))

        await asyncio.gather(*tasks, self.execute(query))


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

    async def get_sub_articles(self, article_ids: Iterable[UUID] | None = None) -> list[SubArticleDTO]:
        query = select(self.sub_article.__table__)
        if article_ids:
            query = query.where(self.sub_article.article_id.in_(article_ids))

        sub_articles = await self.fetch_all(query)
        sub_article_ids = {i.id for i in sub_articles}

        sub_article_imgs = await self.fetch_all(
            select(self.sub_article_img.__table__).where(
                self.sub_article_img.sub_article_id.in_(sub_article_ids),
            ),
        )

        img_map: dict[UUID, list[str]] = defaultdict(list)
        for i in sub_article_imgs:
            img_map[i.sub_article_id].append(i.url)

        return [
            convert_db_to_sub_article_dto(db_sub_article=sub_article, db_sub_article_imgs=img_map[sub_article.id])
            for sub_article in sub_articles
        ]

    def get_imgs_qs(self, article_ids: Iterable[UUID] | None = None) -> Select[Any]:
        query = select(self.article_img.url)
        if article_ids:
            query = query.where(self.article_img.article_id.in_(article_ids))
        return query

    def get_tags_qs(self, article_ids: Iterable[UUID] | None = None) -> Select[Any]:
        table = self.tag.__table__
        selected: list[Any] = [self.tag.__table__]

        if article_ids:
            selected.append(self.rel_article_tag.article_id)
            table = table.join(
                self.rel_article_tag.__table__,
                (self.tag.id == self.rel_article_tag.tag_id) & (self.rel_article_tag.article_id.in_(article_ids)),
            )

        return select(*selected).select_from(table)

    async def get_article_by_id(self, article_id: UUID) -> ArticleDTO:
        article_authors_join = self.article.__table__.join(
            self.author.__table__,
            self.article.author_id == self.author.id,
        )
        qs = (
            select(
                self.article.__table__,
                self.author.nickname.label("author_nickname"),
                self.author.name.label("author_name"),
                self.author.lastname.label("author_lastname"),
                self.author.patronymic.label("author_patronymic"),
            )
            .select_from(article_authors_join)
            .where(self.article.id == article_id)
        )
        article = await self.fetch_one(qs)
        if not article:
            raise ArticleIdNotExistError(article_id)

        sub_articles, article_imgs, article_tags = await asyncio.gather(
            self.get_sub_articles({article_id}),
            self.fetch_sequence(self.get_imgs_qs({article_id})),
            self.fetch_all(self.get_tags_qs({article_id})),
        )

        return convert_db_to_article_dto(article, sub_articles, article_imgs, article_tags)

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
