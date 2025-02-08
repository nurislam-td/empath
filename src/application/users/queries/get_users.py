from dataclasses import dataclass

from application.common.query import Query, QueryHandler
from application.users.dto.user import PaginatedUserDTO
from application.users.ports.repo import UserReader


@dataclass(frozen=True, slots=True)
class GetUsers(Query[PaginatedUserDTO]):
    page: int
    per_page: int


@dataclass(frozen=True, slots=True)
class GetUsersHandler(QueryHandler[GetUsers, PaginatedUserDTO]):
    _user_reader: UserReader

    async def __call__(self, query: GetUsers) -> PaginatedUserDTO:
        return await self._user_reader.get_paginated_users(
            page=query.page, per_page=query.per_page
        )
