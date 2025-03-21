from litestar.dto import DataclassDTO
from litestar.dto.config import DTOConfig

from application.articles.commands.create_article import CreateArticle
from application.articles.commands.edit_article import EditArticle


class ArticleCreateSchema(DataclassDTO[CreateArticle]):
    config = DTOConfig(
        exclude={
            "id",
            "views_cnt",
            "likes_cnt",
            "dislikes_cnt",
            "sub_articles.0.id",
            "author_id",
        },
        rename_strategy="camel",
    )


class EditArticleSchema(DataclassDTO[EditArticle]):
    config = DTOConfig(
        exclude={
            "id",
            "author_id",
        },
        rename_strategy="camel",
        partial=True,
    )
