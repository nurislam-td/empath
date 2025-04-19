from typing import ClassVar
from uuid import UUID

from dishka import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import Controller, Request, Response, delete, get, patch, post, put, status_codes
from litestar.datastructures import State
from litestar.di import Provide
from litestar.dto import DTOData

from articles.api.schemas import (
    ArticleCreateSchema,
    CreateCommentSchema,
    EditArticleSchema,
    EditCommentSchema,
    GetArticleFilters,
)
from articles.application.commands.cancel_dislike_article import CancelDislikeArticle, CancelDislikeArticleHandler
from articles.application.commands.cancel_dislike_comment import CancelDislikeComment, CancelDislikeCommentHandler
from articles.application.commands.cancel_like_article import CancelLikeArticle, CancelLikeArticleHandler
from articles.application.commands.cancel_like_comment import CancelLikeComment, CancelLikeCommentHandler
from articles.application.commands.create_article import (
    CreateArticle,
    CreateArticleHandler,
)
from articles.application.commands.create_comment import CreateComment, CreateCommentHandler
from articles.application.commands.delete_article import DeleteArticle, DeleteArticleHandler
from articles.application.commands.delete_comment import DeleteComment, DeleteCommentHandler
from articles.application.commands.dislike_article import DislikeArticle, DislikeArticleHandler
from articles.application.commands.dislike_comment import DislikeComment, DislikeCommentHandler
from articles.application.commands.edit_article import EditArticle, EditArticleHandler
from articles.application.commands.edit_comment import EditComment, EditCommentHandler
from articles.application.commands.like_article import LikeArticle, LikeArticleHandler
from articles.application.commands.like_comment import LikeComment, LikeCommentHandler
from articles.application.commands.view_article import ViewArticle, ViewArticleHandler
from articles.application.dto.article import (
    ArticleDTO,
    CommentDTO,
    PaginatedArticleDTO,
    SpecializationDTO,
    SubArticleDTO,
    TagDTO,
)
from articles.application.exceptions import (
    ArticleIdNotExistError,
    CommentIdNotExistError,
    ContentAuthorMismatchError,
    DislikeAlreadyExistError,
    EmptyArticleUpdatesError,
    LikeAlreadyExistError,
    NothingToCancelError,
    ViewAlreadyExistError,
)
from articles.application.queries.get_article_by_id import GetArticleById, GetArticleByIdHandler
from articles.application.queries.get_articles import ArticleFilter, GetArticles, GetArticlesHandler
from articles.application.queries.get_comments import GetComments, GetCommentsHandler
from articles.application.queries.get_specialization import GetSpecializations, GetSpecializationsHandler
from articles.application.queries.get_tag_list import GetTagList, GetTagListHandler
from articles.domain.entities.article import EmptyTagListError
from articles.domain.value_objects.article_title import TooLongArticleTitleError
from articles.domain.value_objects.tag_name import TooLongTagNameError
from auth.api.schemas import JWTUserPayload
from common.api.exception_handlers import error_handler
from common.application.dto import PaginatedDTO
from common.application.query import PaginationParams


class ArticleController(Controller):
    exception_handlers: ClassVar = {  # type: ignore  # noqa: PGH003
        TooLongArticleTitleError: error_handler(status_codes.HTTP_422_UNPROCESSABLE_ENTITY),
        TooLongTagNameError: error_handler(status_codes.HTTP_422_UNPROCESSABLE_ENTITY),
        EmptyTagListError: error_handler(status_code=status_codes.HTTP_422_UNPROCESSABLE_ENTITY),
        EmptyArticleUpdatesError: error_handler(status_codes.HTTP_422_UNPROCESSABLE_ENTITY),
        ContentAuthorMismatchError: error_handler(status_codes.HTTP_403_FORBIDDEN),
        DislikeAlreadyExistError: error_handler(status_codes.HTTP_409_CONFLICT),
        LikeAlreadyExistError: error_handler(status_codes.HTTP_409_CONFLICT),
        ViewAlreadyExistError: error_handler(status_codes.HTTP_409_CONFLICT),
        NothingToCancelError: error_handler(status_codes.HTTP_409_CONFLICT),
        CommentIdNotExistError: error_handler(status_codes.HTTP_404_NOT_FOUND),
        ArticleIdNotExistError: error_handler(status_codes.HTTP_404_NOT_FOUND),
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

    @get("/", status_code=status_codes.HTTP_200_OK, dependencies={"filters": Provide(GetArticleFilters)})
    @inject
    async def get_articles(
        self,
        get_articles: Depends[GetArticlesHandler],
        filters: GetArticleFilters,
        pagination_params: PaginationParams,
        request: Request[JWTUserPayload, str, State],
        search: str | None = None,
    ) -> PaginatedArticleDTO:
        return await get_articles(
            GetArticles(
                pagination=pagination_params,
                articles_filter=ArticleFilter(
                    search=search,
                    liked_user_id=request.user.sub if filters.liked else None,
                    disliked_user_id=request.user.sub if filters.disliked else None,
                    viewed_user_id=request.user.sub if filters.viewed else None,
                    specializations_id=filters.specializations_id,
                    exclude_words=filters.exclude_words,
                    include_words=filters.include_words,
                    tags_id=filters.tags_id,
                ),
            ),
        )

    @get("/{article_id:uuid}", status_code=status_codes.HTTP_200_OK)
    @inject
    async def get_article_by_id(
        self,
        get_article: Depends[GetArticleByIdHandler],
        article_id: UUID,
    ) -> ArticleDTO:
        return await get_article(
            GetArticleById(article_id=article_id),
        )

    @delete("/{article_id:uuid}")
    @inject
    async def delete_article(self, article_id: UUID, delete_article: Depends[DeleteArticleHandler]) -> None:
        await delete_article(DeleteArticle(article_id=article_id))

    @post(
        "/{article_id:uuid}/comments",
        status_code=status_codes.HTTP_201_CREATED,
        dto=CreateCommentSchema,
    )
    @inject
    async def create_comment(
        self,
        article_id: UUID,
        data: DTOData[CreateComment],
        create_comment: Depends[CreateCommentHandler],
        request: Request[JWTUserPayload, str, State],
    ) -> Response[str]:
        await create_comment(data.create_instance(author_id=request.user.sub, article_id=article_id))
        return Response(content="", status_code=status_codes.HTTP_201_CREATED)

    @put(
        "/{article_id:uuid}/comments/{comment_id:uuid}",
        status_code=status_codes.HTTP_200_OK,
        dto=EditCommentSchema,
    )
    @inject
    async def update_comment(
        self,
        article_id: UUID,
        comment_id: UUID,
        data: DTOData[EditComment],
        edit_comment: Depends[EditCommentHandler],
        request: Request[JWTUserPayload, str, State],
    ) -> Response[str]:
        await edit_comment(data.create_instance(article_id=article_id, author_id=request.user.sub, id=comment_id))
        return Response(content="", status_code=status_codes.HTTP_200_OK)

    @delete(
        "/{article_id:uuid}/comments/{comment_id:uuid}",
        status_code=status_codes.HTTP_204_NO_CONTENT,
    )
    @inject
    async def delete_comment(self, comment_id: UUID, delete_comment: Depends[DeleteCommentHandler]) -> None:
        await delete_comment(DeleteComment(comment_id=comment_id))

    @get(
        "/{article_id:uuid}/comments",
        status_code=status_codes.HTTP_200_OK,
    )
    @inject
    async def get_comments(
        self,
        article_id: UUID,
        get_comments: Depends[GetCommentsHandler],
        pagination_params: PaginationParams,
    ) -> PaginatedDTO[CommentDTO]:
        return await get_comments(GetComments(pagination=pagination_params, article_id=article_id))

    @get(
        "/specializations",
        status_code=status_codes.HTTP_200_OK,
    )
    @inject
    async def get_specializations(
        self,
        get_specializations: Depends[GetSpecializationsHandler],
        pagination_params: PaginationParams,
        name: str | None = None,
    ) -> PaginatedDTO[SpecializationDTO]:
        return await get_specializations(GetSpecializations(pagination=pagination_params, name=name))

    @post(
        "/{article_id:uuid}/likes",
        status_code=status_codes.HTTP_200_OK,
    )
    @inject
    async def like_article(
        self,
        article_id: UUID,
        request: Request[JWTUserPayload, str, State],
        like_article: Depends[LikeArticleHandler],
    ) -> Response[str]:
        await like_article(LikeArticle(id=article_id, user_id=request.user.sub))
        return Response(content="", status_code=status_codes.HTTP_200_OK)

    @delete(
        "/{article_id:uuid}/likes",
        status_code=status_codes.HTTP_200_OK,
    )
    @inject
    async def cancel_like_article(
        self,
        article_id: UUID,
        request: Request[JWTUserPayload, str, State],
        cancel_like_article: Depends[CancelLikeArticleHandler],
    ) -> Response[str]:
        await cancel_like_article(CancelLikeArticle(id=article_id, user_id=request.user.sub))
        return Response(content="", status_code=status_codes.HTTP_200_OK)

    @post(
        "/{article_id:uuid}/dislikes",
        status_code=status_codes.HTTP_200_OK,
    )
    @inject
    async def dislike_article(
        self,
        article_id: UUID,
        request: Request[JWTUserPayload, str, State],
        dislike_article: Depends[DislikeArticleHandler],
    ) -> Response[str]:
        await dislike_article(DislikeArticle(id=article_id, user_id=request.user.sub))
        return Response(content="", status_code=status_codes.HTTP_200_OK)

    @delete(
        "/{article_id:uuid}/dislikes",
        status_code=status_codes.HTTP_200_OK,
    )
    @inject
    async def cancel_dislike_article(
        self,
        article_id: UUID,
        request: Request[JWTUserPayload, str, State],
        cancel_dislike_article: Depends[CancelDislikeArticleHandler],
    ) -> Response[str]:
        await cancel_dislike_article(CancelDislikeArticle(id=article_id, user_id=request.user.sub))
        return Response(content="", status_code=status_codes.HTTP_200_OK)

    @post(
        "/{article_id:uuid}/views",
        status_code=status_codes.HTTP_200_OK,
    )
    @inject
    async def view_article(
        self,
        article_id: UUID,
        request: Request[JWTUserPayload, str, State],
        view_article: Depends[ViewArticleHandler],
    ) -> Response[str]:
        await view_article(ViewArticle(id=article_id, user_id=request.user.sub))
        return Response(content="", status_code=status_codes.HTTP_200_OK)

    @post(
        "/comments/{comment_id:uuid}/likes",
        status_code=status_codes.HTTP_200_OK,
    )
    @inject
    async def like_comment(
        self,
        comment_id: UUID,
        request: Request[JWTUserPayload, str, State],
        like_comment: Depends[LikeCommentHandler],
    ) -> Response[str]:
        await like_comment(LikeComment(id=comment_id, user_id=request.user.sub))
        return Response(content="", status_code=status_codes.HTTP_200_OK)

    @delete(
        "/comments/{comment_id:uuid}/likes",
        status_code=status_codes.HTTP_200_OK,
    )
    @inject
    async def cancel_like_comment(
        self,
        comment_id: UUID,
        request: Request[JWTUserPayload, str, State],
        cancel_like_comment: Depends[CancelLikeCommentHandler],
    ) -> Response[str]:
        await cancel_like_comment(CancelLikeComment(id=comment_id, user_id=request.user.sub))
        return Response(content="", status_code=status_codes.HTTP_200_OK)

    @post(
        "/comments/{comment_id:uuid}/dislikes",
        status_code=status_codes.HTTP_200_OK,
    )
    @inject
    async def dislike_comment(
        self,
        comment_id: UUID,
        request: Request[JWTUserPayload, str, State],
        dislike_comment: Depends[DislikeCommentHandler],
    ) -> Response[str]:
        await dislike_comment(DislikeComment(id=comment_id, user_id=request.user.sub))
        return Response(content="", status_code=status_codes.HTTP_200_OK)

    @delete(
        "/comments/{comment_id:uuid}/dislikes",
        status_code=status_codes.HTTP_200_OK,
    )
    @inject
    async def cancel_dislike_comment(
        self,
        comment_id: UUID,
        request: Request[JWTUserPayload, str, State],
        cancel_dislike_comment: Depends[CancelDislikeCommentHandler],
    ) -> Response[str]:
        await cancel_dislike_comment(CancelDislikeComment(id=comment_id, user_id=request.user.sub))
        return Response(content="", status_code=status_codes.HTTP_200_OK)
