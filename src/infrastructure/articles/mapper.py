from collections.abc import Sequence

from sqlalchemy import RowMapping

from application.articles.dto.article import ArticleDTO, SubArticleDTO, TagDTO, UserDTO


def convert_db_to_sub_article_dto(db_sub_article: RowMapping, db_sub_article_imgs: Sequence[str]) -> SubArticleDTO:
    return SubArticleDTO(
        title=db_sub_article.title,
        text=db_sub_article.text,
        imgs=list(db_sub_article_imgs),
    )


def convert_db_to_tag_dto(db_tag: RowMapping) -> TagDTO:
    return TagDTO(name=db_tag.name, id=db_tag.id)


def convert_db_to_article_dto(
    db_article: RowMapping,
    db_sub_articles: list[SubArticleDTO],
    db_imgs: Sequence[str],
    db_tags: Sequence[RowMapping],
) -> ArticleDTO:
    return ArticleDTO(
        title=db_article.title,
        text=db_article.text,
        author=UserDTO(
            id=db_article.author_id,
            nickname=db_article.author_nickname,
            full_name=f"{db_article.author_name} {db_article.author_lastname} {db_article.author_patronymic}",
        ),
        tags=[convert_db_to_tag_dto(db_tag) for db_tag in db_tags],
        is_visible=db_article.is_visible,
        sub_articles=db_sub_articles,
        views_cnt=db_article.views_cnt,
        likes_cnt=db_article.likes_cnt,
        dislikes_cnt=db_article.dislikes_cnt,
        imgs=list(db_imgs),
        id=db_article.id,
    )
