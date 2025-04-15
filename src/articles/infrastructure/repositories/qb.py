from dataclasses import dataclass
from typing import Any
from uuid import UUID

from sqlalchemy import Select, func, select

from articles.application.queries.get_articles import ArticleFilter
from articles.infrastructure.models import Article, ArticleImg, Specialization, SubArticle, Tag
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
        return qs

    @classmethod
    def get_articles_qs(cls, article_filter: ArticleFilter | None = None) -> Select[Any]:
        article_authors_join = cls._article.__table__.join(
            cls._author.__table__,
            cls._article.author_id == cls._author.id,
        ).outerjoin(cls._specialization.__table__, cls._article.specialization_id == cls._specialization.id)

        qs = (
            select(
                cls._article.__table__,
                cls._author.nickname.label("author_nickname"),
                cls._author.name.label("author_name"),
                cls._author.lastname.label("author_lastname"),
                cls._author.patronymic.label("author_patronymic"),
                cls._author.image.label("author_img"),
                cls._specialization.name.label("specialization_name"),
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
