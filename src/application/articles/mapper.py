from collections.abc import Callable
from typing import Any

from application.articles.dto.article import ArticleDTO, SubArticleDTO, TagDTO
from domain.articles.entities import SubArticle
from domain.articles.entities.article import Article
from domain.articles.entities.tags import Tag
from domain.articles.value_objects import ArticleTitle
from domain.articles.value_objects.tag_name import TagName
from domain.common.constants import Empty


def convert_dto_to_subarticle(dto: SubArticleDTO) -> SubArticle:
    return SubArticle(text=dto.text, title=ArticleTitle(dto.title), imgs=dto.imgs, id=dto.id)


def convert_dto_to_tag(dto: TagDTO) -> Tag:
    return Tag(name=TagName(dto.name), id=dto.id)


def convert_dto_to_article(dto: ArticleDTO) -> Article:
    tags = [convert_dto_to_tag(i) for i in dto.tags]
    sub_articles = (
        [convert_dto_to_subarticle(i) for i in dto.sub_articles] if dto.sub_articles is not Empty.UNSET else []
    )
    dto_dict = dto.to_dict(exclude_unset=True)
    return Article(
        **dto_dict,
        author_id=dto.author.id,
        title=ArticleTitle(dto.title),
        tags=tags,
        sub_articles=sub_articles,
    )


def convert_dict_to_subarticle(data: dict[str, Any]) -> SubArticle:
    return SubArticle(text=data["text"], title=ArticleTitle(data["title"]), imgs=data["imgs"], id=data["id"])


def convert_dict_to_tag(data: dict[str, Any]) -> Tag:
    return Tag(name=TagName(data["name"]), id=data["id"])


convert_strategy: dict[str, Callable[[Any], Any]] = {
    "title": lambda value: ArticleTitle(value),
    "sub_articles": lambda value: [convert_dict_to_subarticle(data) for data in value],
    "tags": lambda value: [convert_dict_to_tag(dto) for dto in value],
}
