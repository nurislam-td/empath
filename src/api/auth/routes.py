from fastapi import APIRouter, Depends, status

from src.api.auth.dependencies import get_login_handler, get_sign_up_handler
from src.application.auth.commands.login import Login, LoginHandler
from src.application.auth.commands.signup import SignUp, SignUpHandler
from src.domain.auth.value_objects.jwt import JWTPair

router = APIRouter(prefix="/auth", tags=["Authorization"])
user_router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/signup",
    responses={
        status.HTTP_201_CREATED: {"model": JWTPair},
    },
    status_code=status.HTTP_201_CREATED,
)
async def sign_up(
    sign_up_command: SignUp,
    sign_up_handler: SignUpHandler = Depends(get_sign_up_handler),
):
    return await sign_up_handler(command=sign_up_command)


@router.post(
    "/login",
    responses={
        status.HTTP_200_OK: {"model": JWTPair},
    },
    status_code=status.HTTP_200_OK,
)
async def login(
    login_command: Login,
    login_command_handler: LoginHandler = Depends(get_login_handler),
):
    return await login_command_handler(command=login_command)
