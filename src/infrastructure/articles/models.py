from uuid import UUID

from sqlalchemy import (
    BigInteger,
    Boolean,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from domain.articles.constants import ARTICLE_TITLE_LEN, TAG_NAME_LEN
from infrastructure.db.models.base import TimedBaseModel


class ArticleBase(TimedBaseModel):
    __abstract__ = True
    __table_args__ = {"schema": "article"}  # noqa: RUF012


class Article(ArticleBase):
    __tablename__ = "article"

    title: Mapped[str] = mapped_column(String(length=ARTICLE_TITLE_LEN))
    text: Mapped[str] = mapped_column(Text)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=False)
    author_id: Mapped[UUID] = mapped_column(ForeignKey("auth.user.id", ondelete="CASCADE"))
    views_cnt: Mapped[int] = mapped_column(BigInteger, default=0)
    likes_cnt: Mapped[int] = mapped_column(BigInteger, default=0)
    dislikes_cnt: Mapped[int] = mapped_column(BigInteger, default=0)


class Tag(ArticleBase):
    __tablename__ = "tag"

    name: Mapped[str] = mapped_column(String(TAG_NAME_LEN), unique=True)


class RelArticleTag(ArticleBase):
    __tablename__ = "rel_article_tag"
    id: None = None  # type: ignore  # noqa: PGH003

    article_id: Mapped[UUID] = mapped_column(ForeignKey("article.article.id", ondelete="CASCADE"), primary_key=True)
    tag_id: Mapped[UUID] = mapped_column(ForeignKey("article.tag.id", ondelete="CASCADE"), primary_key=True)


class ArticleImg(ArticleBase):
    __tablename__ = "article_img"

    url: Mapped[str] = mapped_column(Text)
    article_id: Mapped[UUID] = mapped_column(ForeignKey("article.article.id", ondelete="CASCADE"))


class SubArticle(ArticleBase):
    __tablename__ = "sub_article"

    article_id: Mapped[UUID] = mapped_column(ForeignKey("article.article.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(ARTICLE_TITLE_LEN))
    text: Mapped[str] = mapped_column(Text)


class SubArticleImg(ArticleBase):
    __tablename__ = "sub_article_img"

    url: Mapped[str] = mapped_column(Text)
    sub_article_id: Mapped[UUID] = mapped_column(ForeignKey("article.sub_article.id", ondelete="CASCADE"))



class Comment(ArticleBase):
    __tablename__ = "comment"

    text: Mapped[str] = mapped_column(Text)
    article_id: Mapped[UUID] = mapped_column(ForeignKey("article.article.id", ondelete="CASCADE"))
    like_cnt: Mapped[int] = mapped_column(BigInteger, default=0)
    dislikes_cnt: Mapped[int] = mapped_column(BigInteger, default=0)
