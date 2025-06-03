from dataclasses import dataclass
from typing import Any
from uuid import UUID

from sqlalchemy import Select, exists, func, or_, select, true

from articles.application.queries.get_articles import ArticleFilter
from articles.infrastructure.models import (
    Article,
    ArticleImg,
    RelArticleTag,
    RelArticleUserDislike,
    RelArticleUserLike,
    RelArticleUserView,
    Specialization,
    SubArticle,
    Tag,
)
from auth.infrastructure.models import User


@dataclass
class TagFilters:
    name: str | None = None

    def filter_qs(self, qs: Select[Any]) -> Select[Any]:
        if self.name:
            qs = qs.where(Tag.name.ilike(f"%{self.name}%")).order_by(
                func.similarity(Tag.name, self.name).desc(),
            )
        return qs


class ArticleQueryBuilder:
    _article = Article
    _article_img = ArticleImg
    _author = User
    _sub_article = SubArticle
    _specialization = Specialization
    _like = RelArticleUserLike
    _dislike = RelArticleUserDislike
    _view = RelArticleUserView
    _tag = Tag
    _rel_tag_article = RelArticleTag

    @classmethod
    def _filter_article(cls, qs: Select[Any], article_filter: ArticleFilter) -> Select[Any]:
        if search := article_filter.search:
            search_qs = select(cls._sub_article.article_id).where(
                cls._sub_article.title.ilike(f"%{search}%") | cls._sub_article.text.ilike(f"%{search}%")
            )
            search_filter = (
                cls._article.title.ilike(f"%{search}%")
                | cls._article.text.ilike(f"%{search}%")
                | cls._article.id.in_(search_qs)
            )
            qs = qs.where(search_filter)
            qs = qs.order_by(cls._article.created_at.desc())
        if article_filter.liked_user_id:
            qs = qs.join(
                cls._like.__table__,
                (cls._article.id == cls._like.article_id) & (cls._like.user_id == article_filter.liked_user_id),
            )
        if article_filter.disliked_user_id:
            qs = qs.join(
                cls._dislike.__table__,
                (cls._article.id == cls._dislike.article_id)
                & (cls._dislike.user_id == article_filter.disliked_user_id),
            )
        if article_filter.viewed_user_id:
            qs = qs.join(
                cls._view.__table__,
                (cls._article.id == cls._view.article_id) & (cls._view.user_id == article_filter.viewed_user_id),
            )
        if article_filter.specializations_id:
            qs = qs.where(cls._article.specialization_id.in_(article_filter.specializations_id))
        if article_filter.tags_id:
            tag_qs = select(cls._rel_tag_article.article_id).join(
                cls._tag.__table__,
                (cls._tag.id == cls._rel_tag_article.tag_id) & (cls._tag.id.in_(article_filter.tags_id)),
            )
            qs = qs.where(cls._article.id.in_(tag_qs))
        if article_filter.exclude_words:
            for word in article_filter.exclude_words:
                qs = qs.where(cls._article.title.not_ilike(f"%{word}%"))
                qs = qs.where(cls._article.text.not_ilike(f"%{word}%"))
                qs = qs.where(
                    cls._article.id.in_(
                        select(cls._sub_article.article_id)
                        .where(cls._sub_article.text.not_ilike(f"%{word}%"))
                        .where(cls._sub_article.title.not_ilike(f"%{word}%")),
                    ),
                )
        if article_filter.include_words:
            conditions = [
                cls._article.title.ilike(f"%{word}%")
                | cls._article.text.ilike(f"%{word}%")
                | cls._article.id.in_(
                    select(cls._sub_article.article_id).where(
                        cls._sub_article.text.ilike(f"%{word}%") | cls._sub_article.title.ilike(f"%{word}%"),
                    )
                )
                for word in article_filter.include_words
            ]
            qs = qs.where(or_(*conditions))
        return qs

    @classmethod
    def get_articles_qs(cls, user_id: UUID | None = None, article_filter: ArticleFilter | None = None) -> Select[Any]:
        article_authors_join = cls._article.__table__.join(
            cls._author.__table__,
            cls._article.author_id == cls._author.id,
        ).outerjoin(cls._specialization.__table__, cls._article.specialization_id == cls._specialization.id)
        is_liked_subq = select(
            exists()
            .where(cls._like.article_id == cls._article.id, cls._like.user_id == user_id)
            .correlate(cls._article),
        ).scalar_subquery()

        is_disliked_subq = select(
            exists()
            .where(cls._dislike.article_id == cls._article.id, cls._dislike.user_id == user_id)
            .correlate(cls._article),
        ).scalar_subquery()

        qs = (
            select(
                cls._article.__table__,
                cls._author.nickname.label("author_nickname"),
                cls._author.name.label("author_name"),
                cls._author.lastname.label("author_lastname"),
                cls._author.patronymic.label("author_patronymic"),
                cls._author.image.label("author_img"),
                cls._author.rating.label("author_rating"),
                cls._specialization.name.label("specialization_name"),
                is_liked_subq.label("is_liked"),
                is_disliked_subq.label("is_disliked"),
            )
            .select_from(article_authors_join)
            .order_by(cls._article.created_at.desc())
        )

        if article_filter:
            qs = cls._filter_article(qs=qs, article_filter=article_filter)

        return qs

    @classmethod
    def get_img_urls_qs(cls, article_ids: set[UUID] | None = None) -> Select[Any]:
        query = select(cls._article_img.url)
        if article_ids:
            query = query.where(cls._article_img.article_id.in_(article_ids))
        return query

    @classmethod
    def get_img_qs(cls, article_ids: set[UUID] | None = None) -> Select[Any]:
        query = select(cls._article_img.__table__)
        if article_ids:
            query = query.where(cls._article_img.article_id.in_(article_ids))
        return query

    @classmethod
    def get_specialization_qs(cls, name: str | None = None) -> Select[Any]:
        qs = select(cls._specialization.__table__)
        if name:
            qs = qs.where(cls._specialization.name.ilike(f"%{name}%"))
        return qs
