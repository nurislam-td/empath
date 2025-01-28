from dishka.integrations.litestar import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import Request, get, status_codes
from litestar.controller import Controller
from litestar.datastructures import State
from litestar.di import Provide

from api.auth.schemas import JWTUserPayload
from api.pagination import PaginationParams, pagination_query_params
from application.users.dto.user import PaginatedUserDTO, UserDTO
from application.users.queries.get_users import GetUsers, GetUsersHandler
from application.users.queries.user_by_id import GetUserById, GetUserByIdHandler


class UserController(Controller):
    @get(path="/me", status_code=status_codes.HTTP_200_OK)
    @inject
    async def get_me(
        self,
        request: Request[JWTUserPayload, str, State],
        get_user_by_id: Depends[GetUserByIdHandler],
    ) -> UserDTO:
        user_id = request.user.sub
        query = GetUserById(user_id)
        return await get_user_by_id(query=query)

    @get(
        path="/",
        status_code=status_codes.HTTP_200_OK,
        dependencies={"pagination_params": Provide(pagination_query_params)},
    )
    @inject
    async def get_users(
        self, pagination_params: PaginationParams, get_users: Depends[GetUsersHandler]
    ) -> PaginatedUserDTO:
        return await get_users(
            GetUsers(page=pagination_params.page, per_page=pagination_params.per_page)
        )
