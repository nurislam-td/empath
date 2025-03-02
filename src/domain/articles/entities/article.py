from dataclasses import dataclass, field
from uuid import UUID, uuid4

from domain.articles.entities.sub_article import SubArticle
from domain.articles.entities.tags import Tag
from domain.articles.events import ArticleCreated
from domain.articles.value_objects import ArticleTitle
from domain.common.entities import Aggregate


@dataclass(slots=True)
class Article(Aggregate):
    title: ArticleTitle
    text: str
    tags: list[Tag]
    author_id: UUID
    imgs: list[str] = field(default_factory=list)
    sub_articles: list[SubArticle] = field(default_factory=list)
    is_visible: bool = field(default=False)
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        self.record_event(ArticleCreated(author_id=self.author_id, article_id=self.id))
