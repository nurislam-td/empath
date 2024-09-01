from fastapi import APIRouter, Depends, status

from src.api.auth.dependencies import get_sign_up_handler
from src.application.auth.commands.signup import SignUp, SignUpHandler
from src.application.auth.ports.jwt import JWTPair

router = APIRouter(prefix="/auth", tags=["Authorization"])
user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post(
    "",
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
