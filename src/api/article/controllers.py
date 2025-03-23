from typing import ClassVar
from uuid import UUID

from dishka import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import Controller, Request, Response, delete, get, patch, post, status_codes
from litestar.datastructures import State
from litestar.dto import DTOData
from msgspec import UNSET, ValidationError

from api.article.schemas import ArticleCreateSchema, EditArticleSchema
from api.auth.schemas import JWTUserPayload
from api.exception_handlers import error_handler
from application.articles.commands.create_article import (
    CreateArticle,
    CreateArticleHandler,
)
from application.articles.commands.delete_article import DeleteArticle, DeleteArticleHandler
from application.articles.commands.edit_article import EditArticle, EditArticleHandler
from application.articles.dto.article import PaginatedArticleDTO, SubArticleDTO, TagDTO
from application.articles.exceptions import EmptyArticleUpdatesError
from application.articles.queries.get_articles import GetArticles, GetArticlesHandler
from application.articles.queries.get_tag_list import GetTagList, GetTagListHandler
from application.common.dto import PaginatedDTO
from application.common.query import PaginationParams
from domain.articles.entities.article import EmptyTagListError
from domain.articles.value_objects.article_title import TooLongArticleTitleError
from domain.articles.value_objects.tag_name import TooLongTagNameError


class ArticleController(Controller):
    exception_handlers: ClassVar = {  # type: ignore  # noqa: PGH003
        TooLongArticleTitleError: error_handler(status_codes.HTTP_422_UNPROCESSABLE_ENTITY),
        TooLongTagNameError: error_handler(status_codes.HTTP_422_UNPROCESSABLE_ENTITY),
        EmptyTagListError: error_handler(status_code=status_codes.HTTP_422_UNPROCESSABLE_ENTITY),
        EmptyArticleUpdatesError: error_handler(status_codes.HTTP_422_UNPROCESSABLE_ENTITY),
    }

    @post(
        "/",
        status_code=status_codes.HTTP_201_CREATED,
        dto=ArticleCreateSchema,
    )
    @inject
    async def create_article(
        self,
        data: DTOData[CreateArticle],
        create_article_handler: Depends[CreateArticleHandler],
        request: Request[JWTUserPayload, str, State],
    ) -> Response[str]:
        await create_article_handler(data.create_instance(author_id=request.user.sub))
        return Response(content="", status_code=status_codes.HTTP_201_CREATED)

    @get(
        "/tags",
        status_code=status_codes.HTTP_200_OK,
    )
    @inject
    async def get_tag_list(
        self,
        get_tag_list: Depends[GetTagListHandler],
        pagination_params: PaginationParams,
        name: str | None = None,
    ) -> PaginatedDTO[TagDTO]:
        return await get_tag_list(GetTagList(name=name, pagination=pagination_params))

    @patch(
        "/{article_id:uuid}",
        status_code=status_codes.HTTP_200_OK,
    )
    @inject
    async def edit_article(
        self,
        article_id: UUID,
        data: EditArticleSchema,
        request: Request[JWTUserPayload, str, State],
        edit_article: Depends[EditArticleHandler],
    ) -> Response[str]:
        kwargs = data.to_dict()
        if tags := kwargs.get("tags"):  # .schema.TagSchema
            kwargs["tags"] = [TagDTO(**tag.to_dict()) for tag in tags]
        if sub_articles := kwargs.get("sub_articles"):  # .schema.SubArticleSchema
            kwargs["sub_articles"] = [SubArticleDTO(**sub_article.to_dict()) for sub_article in sub_articles]
        command = EditArticle(id=article_id, author_id=request.user.sub, **kwargs)
        await edit_article(command)
        return Response(content="", status_code=status_codes.HTTP_200_OK)

    @get("/", status_code=status_codes.HTTP_200_OK)
    @inject
    async def get_articles(
        self, get_articles: Depends[GetArticlesHandler], pagination_params: PaginationParams
    ) -> PaginatedArticleDTO:
        return await get_articles(GetArticles(pagination=pagination_params))

    @delete("/{article_id:uuid}")
    @inject
    async def delete_article(self, article_id: UUID, delete_article: Depends[DeleteArticleHandler]) -> None:
        await delete_article(DeleteArticle(article_id=article_id))
