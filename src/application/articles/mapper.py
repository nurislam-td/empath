from collections.abc import Callable
from typing import Any

from application.articles.dto.article import ArticleDTO, SubArticleDTO, TagDTO
from domain.articles.entities import SubArticle
from domain.articles.entities.article import Article
from domain.articles.entities.tags import Tag
from domain.articles.value_objects import ArticleTitle
from domain.articles.value_objects.tag_name import TagName
from domain.common.exceptions import UnexpectedError


def convert_dict_to_subarticle(data: dict[str, Any]) -> SubArticle:
    try:
        return SubArticle(text=data["text"], title=ArticleTitle(data["title"]), imgs=data["imgs"], id=data["id"])
    except KeyError as e:
        msg = f"KeyError: {e}"
        raise UnexpectedError(msg) from e


def convert_dict_to_tag(data: dict[str, Any]) -> Tag:
    try:
        return Tag(name=TagName(data["name"]), id=data["id"])
    except KeyError as e:
        msg = f"KeyError: {e}"
        raise UnexpectedError(msg) from e


convert_strategy: dict[str, Callable[[Any], Any]] = {
    "title": lambda value: ArticleTitle(value),
    "sub_articles": lambda value: [convert_dict_to_subarticle(data) for data in value],
    "tags": lambda value: [convert_dict_to_tag(data) for data in value],
}


def convert_dto_to_subarticle(dto: SubArticleDTO) -> SubArticle:
    return SubArticle(text=dto.text, title=ArticleTitle(dto.title), imgs=dto.imgs, id=dto.id)


def convert_dto_to_tag(dto: TagDTO) -> Tag:
    return Tag(name=TagName(dto.name), id=dto.id)


def convert_dto_to_article(dto: ArticleDTO) -> Article:
    converted_data: dict[str, Any] = {}

    def default_converter(x: Any) -> Any:
        return x

    for key, value in dto.to_dict().items():
        if key == "author":
            continue
        converter = convert_strategy.get(key, default_converter)
        converted_data[key] = converter(value)

    return Article(**converted_data, author_id=dto.author.id)
