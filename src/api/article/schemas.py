from uuid import UUID

from litestar.dto import DataclassDTO
from litestar.dto.config import DTOConfig

from application.articles.dto.article import ArticleDTO


class ArticleCreateSchema(DataclassDTO[ArticleDTO]):
    config = DTOConfig(
        exclude={
            "id",
            "views_cnt",
            "likes_cnt",
            "dislikes_cnt",
            "sub_articles.0.id",
            "tags.0.id",
        },
        rename_strategy="camel",
    )


class ArticleReadSchema(DataclassDTO[ArticleDTO]):
    config = DTOConfig(
        rename_strategy="camel",
    )
