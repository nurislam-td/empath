from dishka import Provider, Scope, from_context, provide

from application.auth.commands.forget_password import ForgetPasswordHandler
from application.auth.commands.login import LoginHandler
from application.auth.commands.refresh import RefreshHandler
from application.auth.commands.reset_email import ResetEmailHandler
from application.auth.commands.reset_password import ResetPasswordHandler
from application.auth.commands.signup import SignUpHandler
from application.auth.commands.signup_email import SignUpEmailHandler
from application.auth.commands.verify_email import VerifyEmailHandler
from application.auth.ports.jwt import JWTManager
from application.auth.ports.pwd_manager import IPasswordManager
from application.auth.ports.repo import AuthReader, AuthRepo, VerifyCodeRepo
from application.common.ports.email_sender import IEmailSender
from config import Settings
from infrastructure.auth.adapters.jwt_manager import PyJWTManager
from infrastructure.auth.adapters.pwd_manager import PasswordManager
from infrastructure.auth.repositories import (
    AlchemyAuthReader,
    AlchemyAuthRepo,
    RedisVerifyCodeRepo,
)
from infrastructure.common.adapters.email_sender import EmailSender


class AuthProvider(Provider):
    scope = Scope.REQUEST
    config = from_context(provides=Settings, scope=Scope.APP)

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
