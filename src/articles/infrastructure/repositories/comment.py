from dataclasses import dataclass
from typing import Any, ClassVar
from uuid import UUID

from sqlalchemy import Select, exists, select, update
from sqlalchemy.dialects.postgresql import insert

from articles.application.commands.create_comment import CreateComment
from articles.application.commands.edit_comment import EditComment
from articles.application.dto.article import (
    CommentDTO,
)
from articles.application.exceptions import CommentIdNotExistError
from articles.application.ports.repo import CommentReader, CommentRepo
from articles.infrastructure.mapper import convert_db_to_comment_dto
from articles.infrastructure.models import Comment, RelCommentUserDislike, RelCommentUserLike
from articles.infrastructure.repositories.comment_stats import AlchemyCommentStatRepo
from auth.infrastructure.models import User
from common.application.dto import PaginatedDTO
from common.application.query import PaginationParams
from common.infrastructure.repositories.base import AlchemyReader, AlchemyRepo
from common.infrastructure.repositories.pagination import AlchemyPaginator


@dataclass(slots=True)
class AlchemyCommentRepo(CommentRepo):
    """Comment Repo"""

    comment: ClassVar[type[Comment]] = Comment

    _base: AlchemyRepo
    _stat: AlchemyCommentStatRepo

    async def create_comment(self, comment: CreateComment) -> None:
        await self._base.execute(
            insert(self.comment).values(comment.to_dict()),
        )

    async def delete_comment(self, comment_id: UUID) -> None:
        await self._base.execute(update(self.comment).filter(self.comment.id == comment_id).values(is_visible=False))

    async def update_comment(self, comment: EditComment) -> None:
        await self._base.execute(
            update(self.comment).filter(self.comment.id == comment.id).values(text=comment.text),
        )

    async def like_comment(self, comment_id: UUID, user_id: UUID) -> None:
        await self._stat.like_comment(comment_id, user_id)

    async def dislike_comment(self, comment_id: UUID, user_id: UUID) -> None:
        await self._stat.dislike_comment(comment_id, user_id)

    async def cancel_like_comment(self, comment_id: UUID, user_id: UUID) -> None:
        await self._stat.cancel_like_comment(comment_id, user_id)

    async def cancel_dislike_comment(self, comment_id: UUID, user_id: UUID) -> None:
        await self._stat.cancel_dislike_comment(comment_id, user_id)


@dataclass(slots=True)
class AlchemyCommentReader(CommentReader):
    """Comment Reader"""

    _comment: ClassVar[type[Comment]] = Comment
    _author: ClassVar[type[User]] = User
    _like: ClassVar[type[RelCommentUserLike]] = RelCommentUserLike
    _dislike: ClassVar[type[RelCommentUserDislike]] = RelCommentUserDislike
    _paginator: ClassVar[type[AlchemyPaginator]] = AlchemyPaginator

    _base: AlchemyReader

    def get_comments_qs(self, user_id: UUID) -> Select[Any]:
        comment_authors_join = self._comment.__table__.join(
            self._author.__table__,
            self._comment.author_id == self._author.id,
        )
        is_liked_subq = select(
            exists()
            .where(self._like.comment_id == self._comment.id, self._like.user_id == user_id)
            .correlate(self._comment),
        ).scalar_subquery()

        is_disliked_subq = select(
            exists()
            .where(self._dislike.comment_id == self._comment.id, self._dislike.user_id == user_id)
            .correlate(self._comment),
        ).scalar_subquery()

        return select(
            self._comment.__table__,
            self._author.nickname.label("author_nickname"),
            self._author.name.label("author_name"),
            self._author.lastname.label("author_lastname"),
            self._author.patronymic.label("author_patronymic"),
            self._author.image.label("author_img"),
            is_disliked_subq.label("is_disliked"),
            is_liked_subq.label("is_liked"),
        ).select_from(comment_authors_join)

    async def get_article_comments(
        self,
        user_id: UUID,
        article_id: UUID,
        pagination: PaginationParams,
    ) -> PaginatedDTO[CommentDTO]:
        qs = self.get_comments_qs(user_id=user_id)
        qs = qs.where(self._comment.article_id == article_id)

        value_count = await self._base.count(qs)
        qs = self._paginator.paginate(qs, pagination.page, pagination.per_page)
        page_count = self._paginator.get_page_count(value_count, pagination.per_page)

        comments = await self._base.fetch_all(qs)

        return PaginatedDTO[CommentDTO](
            count=page_count,
            page=pagination.page,
            results=[convert_db_to_comment_dto(comment) for comment in comments],
        )

    async def get_comment_by_id(self, user_id: UUID, comment_id: UUID) -> CommentDTO:
        qs = self.get_comments_qs(user_id=user_id)
        qs = qs.where(self._comment.id == comment_id)
        comment = await self._base.fetch_one(qs)
        if not comment:
            raise CommentIdNotExistError(comment_id)

        return convert_db_to_comment_dto(comment)
