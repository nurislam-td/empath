from typing import ClassVar

from dishka import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import Controller, Request, Response, post, status_codes
from litestar.datastructures import State
from litestar.dto import DTOData

from api.article.schemas import ArticleCreateSchema
from api.auth.schemas import JWTUserPayload
from api.exception_handlers import error_handler
from application.articles.commands.create_article import (
    CreateArticle,
    CreateArticleHandler,
)
from domain.articles.value_objects.article_title import TooLongArticleTitleError
from domain.articles.value_objects.tag_name import TooLongTagNameError


class ArticleController(Controller):
    exception_handlers: ClassVar = {  # type: ignore  # noqa: PGH003
        TooLongArticleTitleError: error_handler(status_codes.HTTP_422_UNPROCESSABLE_ENTITY),
        TooLongTagNameError: error_handler(status_codes.HTTP_422_UNPROCESSABLE_ENTITY),
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
