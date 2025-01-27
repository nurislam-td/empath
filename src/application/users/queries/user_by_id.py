from dataclasses import dataclass
from uuid import UUID

from application.common.query import Query, QueryHandler
from application.users.dto.user import UserDTO
from application.users.ports.repo import UserReader
from infrastructure.users.mapper import convert_user_entity_to_user_dto


@dataclass(frozen=True, slots=True)
class GetUserById(Query[UserDTO]):
    user_id: UUID


@dataclass(frozen=True, slots=True)
class GetUserByIdHandler(QueryHandler[GetUserById, UserDTO]):
    _user_reader: UserReader

    async def __call__(self, query: GetUserById) -> UserDTO:
        user = await self._user_reader.get_user_by_id(user_id=query.user_id)
        return convert_user_entity_to_user_dto(user=user)
