from dishka import Provider, Scope, provide  # type: ignore  # noqa: PGH003

from articles.application.commands.cancel_dislike_article import CancelDislikeArticleHandler
from articles.application.commands.cancel_like_article import CancelLikeArticleHandler
from articles.application.commands.create_article import CreateArticleHandler
from articles.application.commands.create_comment import CreateCommentHandler
from articles.application.commands.delete_article import DeleteArticleHandler
from articles.application.commands.delete_comment import DeleteCommentHandler
from articles.application.commands.dislike_article import DislikeArticleHandler
from articles.application.commands.edit_article import EditArticleHandler
from articles.application.commands.edit_comment import EditCommentHandler
from articles.application.commands.like_article import LikeArticleHandler
from articles.application.commands.view_article import ViewArticleHandler
from articles.application.ports.repo import ArticleReader, ArticleRepo, CommentReader, CommentRepo
from articles.application.queries.get_article_by_id import GetArticleByIdHandler
from articles.application.queries.get_articles import GetArticlesHandler
from articles.application.queries.get_comments import GetCommentsHandler
from articles.application.queries.get_specialization import GetSpecializationsHandler
from articles.application.queries.get_tag_list import GetTagListHandler
from articles.infrastructure.repositories.article import AlchemyArticleReader, AlchemyArticleRepo
from articles.infrastructure.repositories.article_stats import AlchemyArticleStatRepo
from articles.infrastructure.repositories.comment import AlchemyCommentReader, AlchemyCommentRepo
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
    comment_repo = provide(AlchemyCommentRepo, provides=CommentRepo)
    comment_reader = provide(AlchemyCommentReader, provides=CommentReader)
    article_stat_repo = provide(AlchemyArticleStatRepo)

    create_article = provide(CreateArticleHandler)
    edit_article = provide(EditArticleHandler)
    delete_article = provide(DeleteArticleHandler)
    create_comment = provide(CreateCommentHandler)
    edit_comment = provide(EditCommentHandler)
    delete_comment = provide(DeleteCommentHandler)
    like_article = provide(LikeArticleHandler)
    dislike_article = provide(DislikeArticleHandler)
    cancel_like_article = provide(CancelLikeArticleHandler)
    cancel_dislike_article = provide(CancelDislikeArticleHandler)
    view_article = provide(ViewArticleHandler)

    get_tag_list = provide(GetTagListHandler)
    get_articles = provide(GetArticlesHandler)
    get_comments = provide(GetCommentsHandler)
    get_article_by_id = provide(GetArticleByIdHandler)
    get_specialization = provide(GetSpecializationsHandler)
