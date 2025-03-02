from dataclasses import dataclass, field
from uuid import UUID, uuid4

from domain.articles.entities.sub_article import SubArticle
from domain.articles.entities.tags import Tag
from domain.articles.events import ArticleCreated, ArticleDisliked, ArticleLiked
from domain.articles.value_objects import ArticleTitle
from domain.common.entities import Aggregate


@dataclass(slots=True)
class Article(Aggregate):
    title: ArticleTitle
    text: str
    tags: list[Tag]
    author_id: UUID
    views_cnt: int = field(default=0)
    likes_cnt: int = field(default=0)
    dislikes_cnt: int = field(default=0)
    imgs: list[str] = field(default_factory=list)
    sub_articles: list[SubArticle] = field(default_factory=list)
    is_visible: bool = field(default=False)
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        self.record_event(ArticleCreated(author_id=self.author_id, article_id=self.id))

    def like_article(self, like_owner_id: UUID):
        self.likes_cnt += 1
        self.record_event(ArticleLiked(like_owner_id=like_owner_id, article_id=self.id))

    def dislike_article(self, dislike_owner_id: UUID):
        self.dislikes_cnt += 1
        self.record_event(
            ArticleDisliked(dislike_owner_id=dislike_owner_id, article_id=self.id)
        )
