from dataclasses import dataclass, field
from typing import TypeAlias
from uuid import UUID, uuid4

from application.common.dto import DTO, PaginatedDTO


@dataclass(frozen=True, slots=True)
class SubArticleDTO(DTO):
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
    author_id: UUID
    tags: list[TagDTO]
    is_visible: bool
    imgs: list[str] = field(default_factory=list)
    sub_articles: list[SubArticleDTO] = field(default_factory=list)
    views_cnt: int = field(default=0)
    likes_cnt: int = field(default=0)
    dislikes_cnt: int = field(default=0)
    id: UUID = field(default_factory=uuid4)


PaginatedArticleDTO: TypeAlias = PaginatedDTO[ArticleDTO]
