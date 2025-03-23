from dishka import Provider, Scope, provide  # type: ignore  # noqa: PGH003

from application.articles.commands.create_article import CreateArticleHandler
from application.articles.commands.delete_article import DeleteArticleHandler
from application.articles.commands.edit_article import EditArticleHandler
from application.articles.ports.repo import ArticleReader, ArticleRepo
from application.articles.queries.get_articles import GetArticlesHandler
from application.articles.queries.get_tag_list import GetTagListHandler
from infrastructure.articles.repositories.article import AlchemyArticleReader, AlchemyArticleRepo


class ArticleProvider(Provider):
    scope = Scope.REQUEST

    article_repo = provide(AlchemyArticleRepo, provides=ArticleRepo)
    article_reader = provide(AlchemyArticleReader, provides=ArticleReader)

    create_article = provide(CreateArticleHandler)
    edit_article = provide(EditArticleHandler)
    delete_article = provide(DeleteArticleHandler)

    get_tag_list = provide(GetTagListHandler)
    get_articles = provide(GetArticlesHandler)
