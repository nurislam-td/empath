from dataclasses import dataclass, field
from uuid import UUID, uuid4

from common.domain.entities import Entity


@dataclass(slots=True)
class Comment(Entity):
    text: str
    article_id: UUID
    author_id: UUID
    id: UUID = field(default_factory=uuid4)
