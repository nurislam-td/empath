import asyncio
import contextlib
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError

from articles.application.exceptions import (
    DislikeAlreadyExistError,
    LikeAlreadyExistError,
    NothingToCancelError,
)
from articles.infrastructure.models import (
    Comment,
    RelCommentUserDislike,
    RelCommentUserLike,
)
from common.infrastructure.repositories.base import AlchemyReader, AlchemyRepo


class AlchemyCommentStatRepo:
    _like = RelCommentUserLike
    _dislike = RelCommentUserDislike
    _comment = Comment

    def __init__(self, base: AlchemyRepo, reader: AlchemyReader) -> None:
        self.base = base
        self.reader = reader

    async def cancel_dislike_comment(self, comment_id: UUID, user_id: UUID) -> None:
        if not await self.reader.fetch_one(
            select(self._dislike).where((self._dislike.comment_id == comment_id) & (self._dislike.user_id == user_id)),
        ):
            raise NothingToCancelError
        await asyncio.gather(
            self.base.execute(
                update(self._comment)
                .values(dislikes_cnt=self._comment.dislikes_cnt - 1)
                .where(self._comment.id == comment_id),
            ),
            self.base.execute(
                delete(self._dislike).where(
                    (self._dislike.comment_id == comment_id) & (self._dislike.user_id == user_id)
                ),
            ),
        )

    async def cancel_like_comment(self, comment_id: UUID, user_id: UUID) -> None:
        if not await self.reader.fetch_one(
            select(self._like).where((self._like.comment_id == comment_id) & (self._like.user_id == user_id)),
        ):
            raise NothingToCancelError
        await asyncio.gather(
            self.base.execute(
                delete(self._like).where((self._like.comment_id == comment_id) & (self._like.user_id == user_id)),
            ),
            self.base.execute(
                update(self._comment)
                .values(like_cnt=self._comment.like_cnt - 1)
                .where(self._comment.id == comment_id),
            ),
        )

    async def like_comment(self, comment_id: UUID, user_id: UUID) -> None:
        try:
            await self.base.execute(
                insert(self._like).values({"comment_id": comment_id, "user_id": user_id}),
            )
        except IntegrityError as e:
            raise LikeAlreadyExistError from e

        await self.base.execute(
            update(self._comment).values(like_cnt=self._comment.like_cnt + 1).where(self._comment.id == comment_id),
        )

    async def dislike_comment(self, comment_id: UUID, user_id: UUID) -> None:
        try:
            await self.base.execute(
                insert(self._dislike).values({"comment_id": comment_id, "user_id": user_id}),
            )
        except IntegrityError as e:
            raise DislikeAlreadyExistError from e

        await self.base.execute(
            update(self._comment)
            .values(dislikes_cnt=self._comment.dislikes_cnt + 1)
            .where(self._comment.id == comment_id),
        )
