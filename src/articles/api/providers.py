from dishka import Provider, Scope, provide  # type: ignore  # noqa: PGH003

from articles.application.commands.create_article import CreateArticleHandler
from articles.application.commands.delete_article import DeleteArticleHandler
from articles.application.commands.edit_article import EditArticleHandler
from articles.application.ports.repo import ArticleReader, ArticleRepo
from articles.application.queries.get_articles import GetArticlesHandler
from articles.application.queries.get_tag_list import GetTagListHandler
from articles.infrastructure.repositories.article import AlchemyArticleReader, AlchemyArticleRepo
from articles.infrastructure.repositories.sub_article import AlchemySubArticleReader, AlchemySubArticleRepo
from articles.infrastructure.repositories.tag import AlchemyTagReader, AlchemyTagRepo


class ArticleProvider(Provider):
    scope = Scope.REQUEST

    article_repo = provide(AlchemyArticleRepo, provides=ArticleRepo)
    article_reader = provide(AlchemyArticleReader, provides=ArticleReader)
    sub_article_repo = provide(AlchemySubArticleRepo)
    sub_article_reader = provide(AlchemySubArticleReader)
    tag_repo = provide(AlchemyTagRepo)
    tag_reader = provide(AlchemyTagReader)

    create_article = provide(CreateArticleHandler)
    edit_article = provide(EditArticleHandler)
    delete_article = provide(DeleteArticleHandler)

    get_tag_list = provide(GetTagListHandler)
    get_articles = provide(GetArticlesHandler)
