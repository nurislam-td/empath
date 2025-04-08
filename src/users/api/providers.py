from dishka import Provider, Scope, provide  # type: ignore  # noqa: PGH003

from common.application.ports.file_storage import FileStorage
from common.infrastructure.adapters.file_storage import S3FileStorage
from users.application.commands.update_avatar import UpdateAvatarHandler
from users.application.commands.update_fullname import UpdateFullnameHandler
from users.application.commands.update_user import UpdateUserHandler
from users.application.ports.repo import UserReader, UserRepo
from users.application.queries.get_users import GetUsersHandler
from users.application.queries.user_by_id import GetUserByIdHandler
from users.infrastructure.repositories.user import AlchemyUserReader, AlchemyUserRepo


class UsersProvider(Provider):
    scope = Scope.REQUEST

    user_reader = provide(AlchemyUserReader, provides=UserReader)
    user_repo = provide(AlchemyUserRepo, provides=UserRepo)
    file_storage = provide(S3FileStorage, provides=FileStorage)

    get_me = provide(GetUserByIdHandler)
    get_users = provide(GetUsersHandler)
    update_avatar = provide(UpdateAvatarHandler)
    update_user = provide(UpdateUserHandler)
    update_fullname = provide(UpdateFullnameHandler)
