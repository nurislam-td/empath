from dishka import Provider, Scope, provide  # type: ignore

from application.articles.commands.create_article import CreateArticleHandler
from application.articles.ports.repo import ArticleReader, ArticleRepo


class ArticleProvider(Provider):
    scope = Scope.REQUEST

    article_repo = provide(..., provides=ArticleRepo)
    article_reader = provide(..., provides=ArticleReader)

    create_article = provide(CreateArticleHandler)
