from dataclasses import dataclass, field
from uuid import UUID, uuid4

from common.application.dto import DTO, PaginatedDTO


@dataclass(frozen=True, slots=True)
class UserDTO(DTO):
    id: UUID
    nickname: str
    img: str | None = None
    full_name: str | None = None


@dataclass(frozen=True, slots=True)
class CommentDTO(DTO):
    text: str
    article_id: UUID
    author: UserDTO
    id: UUID = field(default_factory=uuid4)


@dataclass(frozen=True, slots=True)
class SubArticleDTO(DTO):
    title: str
    text: str
    imgs: list[str] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)


@dataclass(frozen=True, slots=True)
class SubArticleWithArticleIdDTO(DTO):
    article_id: UUID
    title: str
    text: str
    imgs: list[str] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)


@dataclass(frozen=True, slots=True)
class TagDTO(DTO):
    name: str
    id: UUID = field(default_factory=uuid4)


@dataclass(frozen=True, slots=True)
class ArticleDTO(DTO):
    title: str
    text: str
    author: UserDTO
    tags: list[TagDTO]
    is_visible: bool
    imgs: list[str] = field(default_factory=list)
    sub_articles: list[SubArticleDTO] = field(default_factory=list)
    views_cnt: int = 0
    likes_cnt: int = 0
    dislikes_cnt: int = 0
    id: UUID = field(default_factory=uuid4)


type PaginatedArticleDTO = PaginatedDTO[ArticleDTO]
