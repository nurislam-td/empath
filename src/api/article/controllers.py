import pprint

from litestar import Controller, post, status_codes

from api.article.schemas import ArticleCreateSchema, ArticleReadSchema
from application.articles.dto.article import ArticleDTO
from application.articles.mapper import convert_dto_to_article


class ArticleController(Controller):
    @post(
        "/",
        status_code=status_codes.HTTP_201_CREATED,
        exclude_from_auth=True,
        dto=ArticleCreateSchema,
        return_dto=ArticleReadSchema,
    )
    async def create_article(
        self,
        data: ArticleDTO,
        # create_article_handler: Depends[CreateArticleHandler],
    ) -> ArticleDTO:
        pprint.pprint(convert_dto_to_article(data))
        return data
