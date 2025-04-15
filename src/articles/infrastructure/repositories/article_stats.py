from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert

from articles.infrastructure.models import (
    RelArticleUserDislike,
    RelArticleUserLike,
    RelArticleUserView,
)
from common.infrastructure.repositories.base import AlchemyRepo


class AlchemyArticleStatRepo:
    _like = RelArticleUserLike
    _dislike = RelArticleUserDislike
    _view = RelArticleUserView

    def __init__(self, base: AlchemyRepo) -> None:
        self.base = base

    async def cancel_dislike_article(self, article_id: UUID, user_id: UUID) -> None:
        await self.base.execute(
            delete(self._dislike).where((self._dislike.article_id == article_id) & (self._dislike.user_id == user_id)),
        )

    async def cancel_like_article(self, article_id: UUID, user_id: UUID) -> None:
        await self.base.execute(
            delete(self._like).where((self._like.article_id == article_id) & (self._like.user_id == user_id)),
        )

    async def like_article(self, article_id: UUID, user_id: UUID) -> None:
        await self.cancel_dislike_article(article_id=article_id, user_id=user_id)
        await self.base.execute(
            insert(self._like).values({"article_id": article_id, "user_id": user_id}),
        )

    async def dislike_article(self, article_id: UUID, user_id: UUID) -> None:
        await self.cancel_like_article(article_id=article_id, user_id=user_id)
        await self.base.execute(
            insert(self._dislike).values({"article_id": article_id, "user_id": user_id}),
        )

    async def view_article(self, article_id: UUID, user_id: UUID) -> None:
        await self.base.execute(
            insert(self._view).values({"article_id": article_id, "user_id": user_id}),
        )
