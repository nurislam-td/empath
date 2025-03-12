from dishka import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import Controller, Response, post, status_codes

from api.article.schemas import ArticleCreateSchema
from application.articles.commands.create_article import (
    CreateArticle,
    CreateArticleHandler,
)


class ArticleController(Controller):
    @post(
        "/",
        status_code=status_codes.HTTP_201_CREATED,
        dto=ArticleCreateSchema,
        exclude_from_auth=True,
    )
    @inject
    async def create_article(
        self,
        data: CreateArticle,
        create_article_handler: Depends[CreateArticleHandler],
    ) -> Response[None]:
        await create_article_handler(data)
        return Response(content=None, status_code=status_codes.HTTP_201_CREATED)
