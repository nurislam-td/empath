from dishka import Provider, Scope, provide  # type: ignore

from auth.application.commands.forget_password import ForgetPasswordHandler
from auth.application.commands.login import LoginHandler
from auth.application.commands.logout import LogoutHandler
from auth.application.commands.refresh import RefreshHandler
from auth.application.commands.reset_email import ResetEmailHandler
from auth.application.commands.reset_password import ResetPasswordHandler
from auth.application.commands.signup import SignUpHandler
from auth.application.commands.signup_email import SignUpEmailHandler
from auth.application.commands.verify_email import VerifyEmailHandler
from auth.application.ports.jwt import JWTManager
from auth.application.ports.pwd_manager import IPasswordManager
from auth.application.ports.repo import AuthReader, AuthRepo, VerifyCodeRepo
from auth.infrastructure.adapters.jwt_manager import PyJWTManager
from auth.infrastructure.adapters.pwd_manager import PasswordManager
from auth.infrastructure.repositories import (
    AlchemyAuthReader,
    AlchemyAuthRepo,
    RedisVerifyCodeRepo,
)
from common.application.ports.email_sender import IEmailSender
from common.infrastructure.adapters.email_sender import EmailSender
from config import Settings
from users.application.ports.repo import UserReader, UserRepo
from users.infrastructure.repositories.user import AlchemyUserReader, AlchemyUserRepo


class AuthProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def provide_jwt_manager(self, config: Settings) -> JWTManager:
        auth_config = config.app.auth
        return PyJWTManager(
            jwt_alg=auth_config.JWT_ALG,
            access_private_path=auth_config.ACCESS_PRIVATE_PATH,
            access_public_path=auth_config.ACCESS_PUBLIC_PATH,
            access_token_expire=auth_config.ACCESS_TOKEN_EXPIRE,
            refresh_private_path=auth_config.REFRESH_PRIVATE_PATH,
            refresh_public_path=auth_config.REFRESH_PUBLIC_PATH,
            refresh_token_expire=auth_config.REFRESH_TOKEN_EXPIRE,
        )

    auth_repo = provide(AlchemyAuthRepo, provides=AuthRepo)
    auth_reader = provide(AlchemyAuthReader, provides=AuthReader)
    verify_code_repo = provide(RedisVerifyCodeRepo, provides=VerifyCodeRepo)
    user_reader = provide(AlchemyUserReader, provides=UserReader)
    user_repo = provide(AlchemyUserRepo, provides=UserRepo)

    pwd_manager = provide(PasswordManager, provides=IPasswordManager)
    email_sender = provide(EmailSender, provides=IEmailSender)

    login_handler = provide(LoginHandler)
    signup_handler = provide(SignUpHandler)
    signup_email_send = provide(SignUpEmailHandler)
    reset_email_send = provide(ResetEmailHandler)
    verify_email = provide(VerifyEmailHandler)
    reset_password = provide(ResetPasswordHandler)
    forget_password = provide(ForgetPasswordHandler)
    refresh_token = provide(RefreshHandler)
    logout_handler = provide(LogoutHandler)
