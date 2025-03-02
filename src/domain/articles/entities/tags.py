from dataclasses import dataclass, field
from uuid import UUID, uuid4

from domain.articles.value_objects import TagName
from domain.common.entities import Entity


@dataclass(slots=True)
class Tag(Entity):
    name: TagName
    id: UUID = field(default_factory=uuid4)
