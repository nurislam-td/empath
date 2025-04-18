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
    ViewAlreadyExistError,
)
from articles.infrastructure.models import (
    Article,
    RelArticleUserDislike,
    RelArticleUserLike,
    RelArticleUserView,
)
from common.infrastructure.repositories.base import AlchemyReader, AlchemyRepo


class AlchemyArticleStatRepo:
    _like = RelArticleUserLike
    _dislike = RelArticleUserDislike
    _view = RelArticleUserView
    _article = Article

    def __init__(self, base: AlchemyRepo, reader: AlchemyReader) -> None:
        self.base = base
        self.reader = reader

    async def cancel_dislike_article(self, article_id: UUID, user_id: UUID) -> None:
        if not await self.reader.fetch_one(
            select(self._dislike).where((self._dislike.article_id == article_id) & (self._dislike.user_id == user_id)),
        ):
            raise NothingToCancelError
        await asyncio.gather(
            self.base.execute(
                update(self._article)
                .values(dislikes_cnt=self._article.dislikes_cnt - 1)
                .where(self._article.id == article_id),
            ),
            self.base.execute(
                delete(self._dislike).where(
                    (self._dislike.article_id == article_id) & (self._dislike.user_id == user_id)
                ),
            ),
        )

    async def cancel_like_article(self, article_id: UUID, user_id: UUID) -> None:
        if not await self.reader.fetch_one(
            select(self._like).where((self._like.article_id == article_id) & (self._like.user_id == user_id)),
        ):
            raise NothingToCancelError
        await asyncio.gather(
            self.base.execute(
                delete(self._like).where((self._like.article_id == article_id) & (self._like.user_id == user_id)),
            ),
            self.base.execute(
                update(self._article)
                .values(likes_cnt=self._article.likes_cnt - 1)
                .where(self._article.id == article_id),
            ),
        )

    async def like_article(self, article_id: UUID, user_id: UUID) -> None:
        with contextlib.suppress(NothingToCancelError):
            await self.cancel_dislike_article(article_id=article_id, user_id=user_id)

        try:
            await self.base.execute(
                insert(self._like).values({"article_id": article_id, "user_id": user_id}),
            )
        except IntegrityError as e:
            raise LikeAlreadyExistError from e

        await self.base.execute(
            update(self._article).values(likes_cnt=self._article.likes_cnt + 1).where(self._article.id == article_id),
        )

    async def dislike_article(self, article_id: UUID, user_id: UUID) -> None:
        with contextlib.suppress(NothingToCancelError):
            await self.cancel_like_article(article_id=article_id, user_id=user_id)

        try:
            await self.base.execute(
                insert(self._dislike).values({"article_id": article_id, "user_id": user_id}),
            )
        except IntegrityError as e:
            raise DislikeAlreadyExistError from e

        await self.base.execute(
            update(self._article)
            .values(dislikes_cnt=self._article.dislikes_cnt + 1)
            .where(self._article.id == article_id),
        )

    async def view_article(self, article_id: UUID, user_id: UUID) -> None:
        try:
            await self.base.execute(
                insert(self._view).values({"article_id": article_id, "user_id": user_id}),
            )
        except IntegrityError as e:
            raise ViewAlreadyExistError from e
        else:
            await self.base.execute(
                update(self._article)
                .values(views_cnt=self._article.views_cnt + 1)
                .where(self._article.id == article_id),
            )
