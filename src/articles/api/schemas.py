from uuid import UUID, uuid4

from litestar.dto import DataclassDTO
from litestar.dto.config import DTOConfig
from msgspec import UNSET, UnsetType, field

from articles.application.commands.create_article import CreateArticle
from articles.application.commands.create_comment import CreateComment
from articles.application.commands.edit_comment import EditComment
from articles.application.dto.article import ArticleDTO, SubArticleDTO, TagDTO
from common.api.schemas import BaseStruct
from common.application.dto import PaginatedDTO


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
    )


TagSchema = type(
    "TagSchema",
    (BaseStruct,),
    {
        "__annotations__": TagDTO.__annotations__ | {"id": UUID | UnsetType},
        "id": field(default_factory=uuid4),
    },
)

SubArticleSchema = type(
    "SubArticleSchema",
    (BaseStruct,),
    {
        "__annotations__": SubArticleDTO.__annotations__ | {"id": UUID | UnsetType},
        "id": field(default_factory=uuid4),
    },
)


class EditArticleSchema(BaseStruct):
    title: str | UnsetType = UNSET
    text: str | UnsetType = UNSET
    tags: list[TagSchema] | UnsetType = UNSET
    is_visible: bool | UnsetType = UNSET
    imgs: list[str] | UnsetType = UNSET
    sub_articles: list[SubArticleSchema] | UnsetType = UNSET


class CreateCommentSchema(DataclassDTO[CreateComment]):
    config = DTOConfig(
        exclude={
            "id",
            "article_id",
            "author_id",
        },
    )


class EditCommentSchema(DataclassDTO[EditComment]):
    config = DTOConfig(
        exclude={
            "id",
            "article_id",
            "author_id",
        },
    )
