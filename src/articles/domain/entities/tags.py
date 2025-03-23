from dataclasses import dataclass, field
from uuid import UUID, uuid4

from articles.domain.value_objects import TagName
from common.domain.entities import Entity


@dataclass(slots=True)
class Tag(Entity):
    name: TagName
    id: UUID = field(default_factory=uuid4)
