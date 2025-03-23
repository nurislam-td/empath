from dishka import Provider, Scope, provide  # type: ignore  # noqa: PGH003

from common.infrastructure.repositories.base import AlchemyReader, AlchemyRepo


class CommonProvider(Provider):
    scope = Scope.REQUEST

    alchemy_repo = provide(AlchemyRepo)
    alchemy_reader = provide(AlchemyReader)
