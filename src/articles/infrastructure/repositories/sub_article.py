import asyncio
from collections.abc import Iterable, Sequence
from uuid import UUID

from sqlalchemy import RowMapping, delete, select
from sqlalchemy.dialects.postgresql import insert

from articles.application.dto.article import (
    SubArticleDTO,
    SubArticleWithArticleIdDTO,
)
from articles.infrastructure.mapper import convert_db_to_sub_article_dto_list
from articles.infrastructure.models import SubArticle, SubArticleImg
from common.infrastructure.repositories.base import AlchemyReader, AlchemyRepo


class AlchemySubArticleRepo:
    """SubArticle Repo"""

    sub_article = SubArticle
    sub_article_img = SubArticleImg

    def __init__(self, base: AlchemyRepo) -> None:
        self.base = base

    async def create_sub_article_imgs(self, sub_article_id: UUID, imgs: list[str]) -> None:
        await self.base.execute(
            insert(self.sub_article_img).values([{"sub_article_id": sub_article_id, "url": url} for url in imgs])
        )

    async def create_sub_articles(self, article_id: UUID, sub_articles: list[SubArticleDTO]) -> None:
        if not sub_articles:
            return

        await self.base.execute(
            insert(self.sub_article).values(
                [
                    {"id": dto.id, "title": dto.title, "text": dto.text, "article_id": article_id}
                    for dto in sub_articles
                ],
            ),
        )

        await asyncio.gather(*(self.create_sub_article_imgs(dto.id, dto.imgs) for dto in sub_articles if dto.imgs))

    async def delete_sub_articles(self, article_id: UUID) -> None:
        await self.base.execute(delete(self.sub_article).filter(self.sub_article.article_id == article_id))

    async def update_sub_articles(self, article_id: UUID, sub_articles: list[SubArticleDTO]) -> None:
        await self.delete_sub_articles(article_id)
        await self.create_sub_articles(article_id=article_id, sub_articles=sub_articles)


class AlchemySubArticleReader:
    """SubArticle Reader"""

    sub_article = SubArticle
    sub_article_img = SubArticleImg

    def __init__(self, base: AlchemyReader) -> None:
        self.base = base

    async def get_sub_article_imgs(self, sub_article_ids: set[UUID]) -> Sequence[RowMapping]:
        return await self.base.fetch_all(
            select(self.sub_article_img.__table__).where(
                self.sub_article_img.sub_article_id.in_(sub_article_ids),
            ),
        )

    async def get_sub_articles(self, article_ids: Iterable[UUID] | None = None) -> list[SubArticleWithArticleIdDTO]:
        query = select(self.sub_article.__table__)

        if article_ids:
            query = query.where(self.sub_article.article_id.in_(article_ids))
        sub_articles = await self.base.fetch_all(query)
        sub_article_ids = {i.id for i in sub_articles}
        sub_article_imgs = await self.get_sub_article_imgs(sub_article_ids)

        return convert_db_to_sub_article_dto_list(sub_articles=sub_articles, sub_article_imgs=sub_article_imgs)
