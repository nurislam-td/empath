from dishka import Provider, Scope, provide  # type: ignore  # noqa: PGH003

from application.articles.commands.create_article import CreateArticleHandler
from application.articles.ports.repo import ArticleReader, ArticleRepo
from infrastructure.articles.repositories.article import AlchemyArticleReader, AlchemyArticleRepo


class ArticleProvider(Provider):
    scope = Scope.REQUEST

    article_repo = provide(AlchemyArticleRepo, provides=ArticleRepo)
    article_reader = provide(AlchemyArticleReader, provides=ArticleReader)

    create_article = provide(CreateArticleHandler)
