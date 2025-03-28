from collections import defaultdict
from collections.abc import Sequence
from typing import TYPE_CHECKING

from sqlalchemy import RowMapping

from articles.application.dto.article import ArticleDTO, SubArticleDTO, SubArticleWithArticleIdDTO, TagDTO, UserDTO

if TYPE_CHECKING:
    from uuid import UUID


def convert_db_to_sub_article_dto_list(
    sub_articles: Sequence[RowMapping], sub_article_imgs: Sequence[RowMapping]
) -> list[SubArticleWithArticleIdDTO]:
    img_map: dict[UUID, list[str]] = defaultdict(list)
    for i in sub_article_imgs:
        img_map[i.sub_article_id].append(i.url)
    return [
        SubArticleWithArticleIdDTO(
            title=sub_article.title,
            text=sub_article.text,
            imgs=list(img_map[sub_article.id]),
            id=sub_article.id,
            article_id=sub_article.id,
        )
        for sub_article in sub_articles
    ]


def convert_db_to_tag_dto(db_tag: RowMapping) -> TagDTO:
    return TagDTO(name=db_tag.name, id=db_tag.id)


def convert_db_to_article_dto(
    article: RowMapping,
    sub_articles: list[SubArticleWithArticleIdDTO],
    imgs: Sequence[str],
    tags: Sequence[RowMapping],
) -> ArticleDTO:
    return ArticleDTO(
        title=article.title,
        text=article.text,
        author=UserDTO(
            id=article.author_id,
            nickname=article.author_nickname,
            full_name=f"{article.author_name} {article.author_lastname} {article.author_patronymic}",
        ),
        tags=[convert_db_to_tag_dto(db_tag) for db_tag in tags],
        is_visible=article.is_visible,
        sub_articles=[
            SubArticleDTO(**{key: value for key, value in sub_article.to_dict().items() if key != "article_id"})
            for sub_article in sub_articles
        ],
        views_cnt=article.views_cnt,
        likes_cnt=article.likes_cnt,
        dislikes_cnt=article.dislikes_cnt,
        imgs=list(imgs),
        id=article.id,
    )


def convert_db_to_article_dto_list(
    articles: Sequence[RowMapping],
    sub_articles: list[SubArticleWithArticleIdDTO],
    tags: Sequence[RowMapping],
    imgs: Sequence[RowMapping],
) -> list[ArticleDTO]:
    tags_map: dict[UUID, list[RowMapping]] = defaultdict(list)
    for tag in tags:
        tags_map[tag.article_id].append(tag)

    sub_articles_map: dict[UUID, list[SubArticleWithArticleIdDTO]] = defaultdict(list)
    for sub_article in sub_articles:
        sub_articles_map[sub_article.article_id].append(sub_article)

    img_map: dict[UUID, list[str]] = defaultdict(list)
    for img in imgs:
        img_map[img.article_id].append(img.url)

    return [
        convert_db_to_article_dto(
            article=article,
            sub_articles=sub_articles_map[article.id],
            imgs=img_map[article.id],
            tags=tags_map[article.id],
        )
        for article in articles
    ]
