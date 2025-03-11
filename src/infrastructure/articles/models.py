from uuid import UUID

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    String,
    Text,
)

from domain.articles.constants import ARTICLE_TITLE_LEN, TAG_NAME_LEN
from infrastructure.db.models.base import TimedBaseModel


class ArticleBase(TimedBaseModel):
    __abstract__ = True
    __table_args__ = {"schema": "article"}


class Article(ArticleBase):
    __tablename__ = "article"

    title = Column(String(length=ARTICLE_TITLE_LEN))
    text = Column(Text)
    is_visible = Column(Boolean, default=False)
    author_id = Column(ForeignKey("auth.user.id", ondelete="CASCADE"))  # type: ignore
    views_cnt = Column(BigInteger, default=0)
    likes_cnt = Column(BigInteger, default=0)
    dislikes_cnt = Column(BigInteger, default=0)


class Tag(ArticleBase):
    __tablename__ = "tag"

    name = Column(String(TAG_NAME_LEN))


class RelArticleTag(ArticleBase):
    __tablename__ = "rel_article_tag"

    id = None  # type: ignore  # noqa: PGH003
    article_id: Column[UUID] = Column(ForeignKey("article.article.id", ondelete="CASCADE"), primary_key=True)
    tag_id: Column[UUID] = Column(ForeignKey("article.tag.id", ondelete="CASCADE"), primary_key=True)


class ArticleImg(ArticleBase):
    __tablename__ = "article_img"

    url = Column(Text)
    article_id: Column[UUID] = Column(ForeignKey("article.article.id", ondelete="CASCADE"))


class SubArticle(ArticleBase):
    __tablename__ = "sub_article"

    article_id: Column[UUID] = Column(ForeignKey("article.article.id", ondelete="CASCADE"))
    title = Column(String(ARTICLE_TITLE_LEN))
    text = Column(Text)


class SubArticleImg(ArticleBase):
    __tablename__ = "sub_article_img"

    url = Column(Text)
    sub_article_id: Column[UUID] = Column(ForeignKey("article.sub_article.id", ondelete="CASCADE"))
