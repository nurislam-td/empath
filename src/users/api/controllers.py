from io import BytesIO
from typing import Annotated
from uuid import UUID

from dishka.integrations.litestar import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import Request, get, put, status_codes
from litestar.controller import Controller
from litestar.datastructures import State, UploadFile
from litestar.enums import RequestEncodingType
from litestar.params import Body
from litestar.response import Response

from auth.api.schemas import JWTUserPayload
from common.application.query import PaginationParams
from users.api.schemas import UserUpdateSchema
from users.application.commands.update_avatar import UpdateAvatar, UpdateAvatarHandler
from users.application.commands.update_user import UpdateUser, UpdateUserHandler
from users.application.dto.user import PaginatedUserDTO, UserDTO
from users.application.queries.get_users import GetUsers, GetUsersHandler
from users.application.queries.user_by_id import GetUserById, GetUserByIdHandler


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
    )
    @inject
    async def get_users(
        self, pagination_params: PaginationParams, get_users: Depends[GetUsersHandler]
    ) -> PaginatedUserDTO:
        return await get_users(GetUsers(page=pagination_params.page, per_page=pagination_params.per_page))

    @put(path="/me/avatar", status_code=status_codes.HTTP_200_OK)
    @inject
    async def update_user_avatar(
        self,
        data: Annotated[UploadFile, Body(media_type=RequestEncodingType.MULTI_PART)],
        update_avatar: Depends[UpdateAvatarHandler],
        request: Request[JWTUserPayload, str, State],
    ) -> Response[str]:
        content = await data.read()
        command = UpdateAvatar(user_id=request.user.sub, file=BytesIO(content), filename=data.filename)
        new_url = await update_avatar(command)
        return Response(content=new_url, status_code=status_codes.HTTP_200_OK)

    @put(path="/{user_id:uuid}", status_code=status_codes.HTTP_200_OK)
    @inject
    async def update_user(
        self,
        data: UserUpdateSchema,
        user_id: UUID,
        update_user: Depends[UpdateUserHandler],
    ) -> Response[None]:
        command = UpdateUser(**data.to_dict(), user_id=user_id)
        await update_user(command)
        return Response(content=None, status_code=status_codes.HTTP_200_OK)
