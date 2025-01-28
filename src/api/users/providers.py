from dishka import Provider, Scope, from_context, provide  # type: ignore

from application.users.ports.repo import UserReader, UserRepo
from application.users.queries.get_users import GetUsersHandler
from application.users.queries.user_by_id import GetUserByIdHandler
from config import Settings
from infrastructure.users.repositories.user import AlchemyUserReader, AlchemyUserRepo


class UsersProvider(Provider):
    scope = Scope.REQUEST
    config = from_context(provides=Settings, scope=Scope.APP)

    user_reader = provide(AlchemyUserReader, provides=UserReader)
    user_repo = provide(AlchemyUserRepo, provides=UserRepo)

    get_me = provide(GetUserByIdHandler)
    get_users = provide(GetUsersHandler)
