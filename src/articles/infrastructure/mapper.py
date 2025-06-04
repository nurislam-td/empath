from collections import defaultdict
from collections.abc import Sequence
from typing import TYPE_CHECKING

from sqlalchemy import RowMapping

from articles.application.dto.article import (
    ArticleDTO,
    CommentDTO,
    ReactionStatus,
    SpecializationDTO,
    SubArticleDTO,
    SubArticleWithArticleIdDTO,
    TagDTO,
    UserDTO,
)

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
            article_id=sub_article.article_id,
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
    author_fullname = " ".join(
        [
            article.author_lastname or "",
            article.author_name or "",
            article.author_patronymic or "",
        ],
    ).strip()

    reaction_status: ReactionStatus = "no_reaction"
    if article.is_liked:
        reaction_status = "is_liked"
    if article.is_disliked:
        reaction_status = "is_disliked"

    return ArticleDTO(
        title=article.title,
        text=article.text,
        author=UserDTO(
            id=article.author_id,
            nickname=article.author_nickname,
            full_name=author_fullname,
            img=article.author_img,
            rating=article.author_rating,
        ),
        tags=[convert_db_to_tag_dto(db_tag) for db_tag in tags],
        is_visible=article.is_visible,
        sub_articles=[
            SubArticleDTO(**{key: value for key, value in sub_article.to_dict().items() if key != "article_id"})
            for sub_article in sub_articles
        ],
        reaction_status=reaction_status,
        views_cnt=article.views_cnt,
        likes_cnt=article.likes_cnt,
        dislikes_cnt=article.dislikes_cnt,
        imgs=list(imgs),
        specialization=SpecializationDTO(name=article.specialization_name, id=article.specialization_id)
        if article.specialization_id
        else None,
        is_viewed=article.is_viewed,
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


def convert_db_to_comment_dto(comment: RowMapping) -> CommentDTO:
    author_fullname = " ".join(
        [
            comment.author_lastname or "",
            comment.author_name or "",
            comment.author_patronymic or "",
        ],
    ).strip()
    reaction_status: ReactionStatus = "no_reaction"
    if comment.is_disliked:
        reaction_status = "is_liked"
    if comment.is_liked:
        reaction_status = "is_liked"
    return CommentDTO(
        text=comment.text,
        article_id=comment.article_id,
        author=UserDTO(
            id=comment.author_id,
            nickname=comment.author_nickname,
            full_name=author_fullname,
            img=comment.author_img,
            rating=comment.author_rating,
        ),
        parent_id=comment.parent_id,
        id=comment.id,
        is_visible=comment.is_visible,
        likes_cnt=comment.like_cnt,
        dislikes_cnt=comment.dislikes_cnt,
        reaction_status=reaction_status,
        created_at=comment.created_at,
    )
