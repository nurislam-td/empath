from uuid import UUID, uuid4

from litestar.dto import DataclassDTO
from litestar.dto.config import DTOConfig
from msgspec import UNSET, UnsetType, field

from application.articles.commands.create_article import CreateArticle
from application.articles.dto.article import SubArticleDTO, TagDTO
from infrastructure.common.schemas import CamelizedBaseStruct


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


TagSchema = type(
    "TagSchema",
    (CamelizedBaseStruct,),
    {
        "__annotations__": TagDTO.__annotations__ | {"id": UUID | UnsetType},
        "id": field(default_factory=uuid4),
    },
)

SubArticleSchema = type(
    "SubArticleSchema",
    (CamelizedBaseStruct,),
    {
        "__annotations__": SubArticleDTO.__annotations__ | {"id": UUID | UnsetType},
        "id": field(default_factory=uuid4),
    },
)


class EditArticleSchema(CamelizedBaseStruct):
    title: str | UnsetType = UNSET
    text: str | UnsetType = UNSET
    tags: list[TagSchema] | UnsetType = UNSET
    is_visible: bool | UnsetType = UNSET
    imgs: list[str] | UnsetType = UNSET
    sub_articles: list[SubArticleSchema] | UnsetType = UNSET
