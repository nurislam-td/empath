import asyncio
from uuid import UUID

from sqlalchemy.dialects.postgresql import insert

from application.articles.dto.article import ArticleDTO, SubArticleDTO
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
        asyncio.gather(
            self.create_sub_articles(article_id=article.id, sub_articles=article.sub_articles),
            self.create_article_imgs(article.id, article.imgs),
        )
        await self.execute(
            insert(self.tag).values([tag.to_dict() for tag in article.tags]).on_conflict_do_nothing(),
        )
        await self.execute(
            insert(self.rel_article_tag).values([{"tag_id": dto.id, "article_id": article.id} for dto in article.tags])
        )


class AlchemyAuthReader(AlchemyReader, ArticleReader):
    """Article Reader implementation."""
