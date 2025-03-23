from uuid import UUID

from attr import dataclass

from common.domain.events import Event


@dataclass(frozen=True, slots=True)
class ArticleLiked(Event):
    like_owner_id: UUID
    article_id: UUID
