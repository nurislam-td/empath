import asyncio
from typing import Any
from uuid import UUID

from sqlalchemy import Select, delete, select
from sqlalchemy.dialects.postgresql import insert

from articles.application.dto.article import TagDTO
from articles.application.ports.repo import ArticleReader, ArticleRepo
from articles.application.queries.get_tag_list import GetTagList
from articles.infrastructure.mapper import convert_db_to_tag_dto
from articles.infrastructure.models import RelArticleTag, Tag
from articles.infrastructure.repositories.qb import TagFilters
from common.application.dto import PaginatedDTO
from common.infrastructure.repositories.base import AlchemyReader, AlchemyRepo
from common.infrastructure.repositories.pagination import AlchemyPaginator


class AlchemyTagRepo:
    """Tag Repo implementation."""

    tag = Tag
    rel_article_tag = RelArticleTag

    def __init__(self, base: AlchemyRepo) -> None:
        self.base = base

    async def create_tags_if_not_exists(self, tags: list[TagDTO]) -> None:
        await self.base.execute(
            insert(self.tag).values([tag.to_dict() for tag in tags]).on_conflict_do_nothing(),
        )

    async def map_tags_to_article(self, tag_ids: set[UUID], article_id: UUID) -> None:
        if not tag_ids:
            return
        await self.base.execute(
            insert(self.rel_article_tag).values([{"tag_id": tag_id, "article_id": article_id} for tag_id in tag_ids])
        )

    async def unmap_tags_from_article(self, article_id: UUID) -> None:
        await self.base.execute(delete(self.rel_article_tag).filter(self.rel_article_tag.article_id == article_id))

    async def update_article_tags(self, article_id: UUID, tags: list[TagDTO]) -> None:
        await asyncio.gather(
            self.unmap_tags_from_article(article_id),
        )
        await self.create_tags_if_not_exists(tags)
        await self.map_tags_to_article({dto.id for dto in tags}, article_id)


class AlchemyTagReader:
    """Tag Reader implementation."""

    paginator = AlchemyPaginator
    tag = Tag
    rel_article_tag = RelArticleTag

    def __init__(self, base: AlchemyReader) -> None:
        self.base = base

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

    async def get_tag_list(self, query: GetTagList) -> PaginatedDTO[TagDTO]:
        qs = self.get_tags_qs()
        qs = TagFilters(name=query.name).filter_qs(qs).order_by(self.tag.name)

        paginated_query = self.paginator.paginate(
            query=qs, page=query.pagination.page, per_page=query.pagination.per_page
        )
        value_count = await self.base.count(qs)
        tags = await self.base.fetch_all(paginated_query)
        if not tags:
            return PaginatedDTO[TagDTO](count=value_count, page=query.pagination.page, results=[])

        return PaginatedDTO[TagDTO](
            count=value_count,
            page=query.pagination.page,
            results=[convert_db_to_tag_dto(tag) for tag in tags],
        )
