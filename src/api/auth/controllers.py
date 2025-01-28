from typing import Annotated

from dishka.integrations.litestar import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import Controller, Request, post, status_codes
from litestar.background_tasks import BackgroundTask
from litestar.datastructures import State
from litestar.dto.dataclass_dto import DataclassDTO
from litestar.response.base import Response

from api.auth.schemas import (
    ForgetPasswordSchema,
    JWTUserPayload,
    LoginSchema,
    RefreshTokenSchema,
    ResetPasswordSchema,
    SignUpSchema,
)
from application.auth.commands import Login, LoginHandler
from application.auth.commands.forget_password import (
    ForgetPassword,
    ForgetPasswordHandler,
)
from application.auth.commands.logout import Logout, LogoutHandler
from application.auth.commands.refresh import Refresh, RefreshHandler
from application.auth.commands.reset_email import ResetEmail, ResetEmailHandler
from application.auth.commands.reset_password import ResetPassword, ResetPasswordHandler
from application.auth.commands.signup import SignUp, SignUpHandler
from application.auth.commands.signup_email import SignUpEmail, SignUpEmailHandler
from application.auth.commands.verify_email import VerifyEmail, VerifyEmailHandler
from domain.auth.value_objects.jwt import JWTPair
from infrastructure.common.schemas import dto_config


class AuthController(Controller):
    @post(
        "/login",
        status_code=status_codes.HTTP_200_OK,
        exclude_from_auth=True,
        return_dto=DataclassDTO[Annotated[JWTPair, dto_config]],
    )
    @inject
    async def login(
        self, data: LoginSchema, login_handler: Depends[LoginHandler]
    ) -> JWTPair:
        login_command = Login(email=data.email, password=data.password)
        return await login_handler(command=login_command)

    @post(
        "/signup",
        status_code=status_codes.HTTP_201_CREATED,
        exclude_from_auth=True,
        return_dto=DataclassDTO[Annotated[JWTPair, dto_config]],
    )
    @inject
    async def signup(
        self,
        data: SignUpSchema,
        signup_handler: Depends[SignUpHandler],
    ) -> JWTPair:
        signup_command = SignUp(data.email, data.password, data.nickname)
        return await signup_handler(signup_command)

    @post(
        "/signup-email",
        status_code=status_codes.HTTP_202_ACCEPTED,
        exclude_from_auth=True,
    )
    @inject
    async def send_signup_email(
        self, email: str, send_signup_email: Depends[SignUpEmailHandler]
    ) -> Response[str]:
        command = SignUpEmail(email=email)
        return Response(
            status_code=status_codes.HTTP_202_ACCEPTED,
            content="",
            background=BackgroundTask(send_signup_email, command),
        )

    @post(
        "/reset-email",
        status_code=status_codes.HTTP_202_ACCEPTED,
        exclude_from_auth=True,
    )
    @inject
    async def send_reset_email(
        self, email: str, send_reset_email: Depends[ResetEmailHandler]
    ) -> Response[str]:
        command = ResetEmail(email=email)
        return Response(
            status_code=status_codes.HTTP_202_ACCEPTED,
            content="",
            background=BackgroundTask(send_reset_email, command),
        )

    @post(
        "/verify-code",
        status_code=status_codes.HTTP_200_OK,
        exclude_from_auth=True,
    )
    @inject
    async def verify_code(
        self, email: str, code: str, verify_email: Depends[VerifyEmailHandler]
    ) -> Response[str]:
        command = VerifyEmail(email=email, code=code)
        await verify_email(command)
        return Response(status_code=status_codes.HTTP_200_OK, content="")

    @post(
        "/password",
        status_code=status_codes.HTTP_200_OK,
    )
    @inject
    async def reset_password(
        self,
        data: ResetPasswordSchema,
        reset_password: Depends[ResetPasswordHandler],
        request: Request[JWTUserPayload, str, State],
    ) -> Response[str]:
        command = ResetPassword(
            old_password=data.old_password,
            new_password=data.new_password,
            user_id=request.user.sub,
        )
        await reset_password(command)
        return Response(status_code=status_codes.HTTP_200_OK, content="")

    @post(
        "/forget-password",
        status_code=status_codes.HTTP_200_OK,
        exclude_from_auth=True,
    )
    @inject
    async def forget_password(
        self,
        data: ForgetPasswordSchema,
        forget_password: Depends[ForgetPasswordHandler],
    ) -> Response[str]:
        command = ForgetPassword(email=data.email, password=data.password)
        await forget_password(command)
        return Response(status_code=status_codes.HTTP_200_OK, content="")

    @post(
        "/refresh-token",
        status_code=status_codes.HTTP_200_OK,
        exclude_from_auth=True,
        return_dto=DataclassDTO[Annotated[JWTPair, dto_config]],
    )
    @inject
    async def refresh_token(
        self, data: RefreshTokenSchema, refresh_token: Depends[RefreshHandler]
    ) -> JWTPair:
        command = Refresh(refresh_token=data.refresh_token)
        return await refresh_token(command=command)

    @post(
        "/logout",
        status_code=status_codes.HTTP_200_OK,
    )
    @inject
    async def logout(
        self,
        request: Request[JWTUserPayload, str, State],
        logout: Depends[LogoutHandler],
    ) -> None:
        user_id = request.user.sub
        command = Logout(user_id=user_id)
        return await logout(command=command)
