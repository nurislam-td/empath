from application.articles.dto.article import ArticleDTO, SubArticleDTO, TagDTO
from domain.articles.entities import SubArticle
from domain.articles.entities.article import Article
from domain.articles.entities.tags import Tag
from domain.articles.value_objects import ArticleTitle
from domain.articles.value_objects.tag_name import TagName


def convert_dto_to_subarticle(dto: SubArticleDTO):
    return SubArticle(
        text=dto.text, title=ArticleTitle(dto.title), imgs=dto.imgs, id=dto.id
    )


def convert_dto_to_tag(dto: TagDTO):
    return Tag(name=TagName(dto.name), id=dto.id)


def convert_dto_to_article(dto: ArticleDTO):
    tags = [convert_dto_to_tag(i) for i in dto.tags]
    sub_articles = (
        [convert_dto_to_subarticle(i) for i in dto.sub_articles]
        if dto.sub_articles
        else []
    )
    return Article(
        title=ArticleTitle(dto.title),
        text=dto.text,
        author_id=dto.author_id,
        tags=tags,
        is_visible=dto.is_visible,
        imgs=dto.imgs,
        sub_articles=sub_articles,
        views_cnt=dto.views_cnt,
        likes_cnt=dto.likes_cnt,
        dislikes_cnt=dto.dislikes_cnt,
        id=dto.id,
    )
