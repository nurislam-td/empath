from dataclasses import dataclass
from typing import Any, ClassVar
from uuid import UUID

from sqlalchemy import Select, delete, select, update
from sqlalchemy.dialects.postgresql import insert

from articles.application.commands.create_comment import CreateComment
from articles.application.commands.edit_comment import EditComment
from articles.application.dto.article import (
    CommentDTO,
)
from articles.application.exceptions import CommentIdNotExistError
from articles.application.ports.repo import CommentReader, CommentRepo
from articles.infrastructure.mapper import convert_db_to_comment_dto
from articles.infrastructure.models import Comment
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

    async def create_comment(self, comment: CreateComment) -> None:
        await self._base.execute(
            insert(self.comment).values(comment.to_dict()),
        )

    async def delete_comment(self, comment_id: UUID) -> None:
        await self._base.execute(delete(self.comment).filter(self.comment.id == comment_id))

    async def update_comment(self, comment: EditComment) -> None:
        await self._base.execute(
            update(self.comment).filter(self.comment.id == comment.id).values(text=comment.text),
        )


@dataclass(slots=True)
class AlchemyCommentReader(CommentReader):
    """Comment Reader"""

    _comment: ClassVar[type[Comment]] = Comment
    _author: ClassVar[type[User]] = User
    _paginator: ClassVar[type[AlchemyPaginator]] = AlchemyPaginator

    _base: AlchemyReader

    def get_comments_qs(self) -> Select[Any]:
        comment_authors_join = self._comment.__table__.join(
            self._author.__table__,
            self._comment.author_id == self._author.id,
        )

        return select(
            self._comment.__table__,
            self._author.nickname.label("author_nickname"),
            self._author.name.label("author_name"),
            self._author.lastname.label("author_lastname"),
            self._author.patronymic.label("author_patronymic"),
            self._author.image.label("author_img"),
        ).select_from(comment_authors_join)

    async def get_article_comments(self, article_id: UUID, pagination: PaginationParams) -> PaginatedDTO[CommentDTO]:
        qs = self.get_comments_qs()
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

    async def get_comment_by_id(self, comment_id: UUID) -> CommentDTO:
        qs = self.get_comments_qs()
        qs = qs.where(self._comment.id == comment_id)
        comment = await self._base.fetch_one(qs)
        if not comment:
            raise CommentIdNotExistError(comment_id)

        return convert_db_to_comment_dto(comment)
