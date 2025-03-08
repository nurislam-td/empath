# ruff: noqa
# pylint: skip-file
# flake8: noqa
# pyright: basic

from .base import BaseModel, TimedBaseModel


def init_all_models():
    from infrastructure.articles.models import (
        Article,
        ArticleBase,
        ArticleImg,
        RelArticleTag,
        SubArticle,
        SubArticleImg,
        Tag,
    )
    from infrastructure.auth.models import RefreshToken, User


__all__ = (
    "BaseModel",
    "TimedBaseModel",
    "init_all_models",
)
