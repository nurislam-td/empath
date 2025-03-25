from dataclasses import dataclass, field
from uuid import UUID, uuid4

from articles.domain.value_objects.article_title import ArticleTitle
from common.domain.entities import Entity


@dataclass(slots=True)
class SubArticle(Entity):
    text: str
    title: ArticleTitle
    imgs: list[str] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)
