from uuid import UUID

from attr import dataclass

from common.domain.events import Event


@dataclass(frozen=True, slots=True)
class ArticleDisliked(Event):
    dislike_owner_id: UUID
    article_id: UUID
