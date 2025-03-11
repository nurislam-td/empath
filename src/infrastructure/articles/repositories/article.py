import asyncio
from collections.abc import Iterable
from uuid import UUID

from sqlalchemy import delete, update
from sqlalchemy.dialects.postgresql import insert

from application.articles.dto.article import ArticleDTO, EditArticleDTO, SubArticleDTO, TagDTO
from application.articles.ports.repo import ArticleReader, ArticleRepo
from infrastructure.articles.models import Article, ArticleImg, RelArticleTag, SubArticle, SubArticleImg, Tag
from infrastructure.db.repositories.base import AlchemyReader, AlchemyRepo


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
                [{"title": dto.title, "text": dto.text, "article_id": article_id} for dto in sub_articles],
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

    async def create_article(self, article: ArticleDTO) -> None:
        await self.execute(
            insert(self.article).values(
                title=article.title,
                text=article.text,
                is_visible=article.is_visible,
                author_id=article.author_id,
                id=article.id,
            ),
        )
        await asyncio.gather(
            self.create_sub_articles(article_id=article.id, sub_articles=article.sub_articles),
            self.create_article_imgs(article.id, article.imgs),
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

    async def update_article(self, article: EditArticleDTO) -> None:
        article_dict = article.to_dict(exclude_unset=True)
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


class AlchemyAuthReader(AlchemyReader, ArticleReader):
    """Article Reader implementation."""
