from typing import Iterable

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
from auth.application.ports.jwt import JWTManager  # type: ignore  # noqa: PGH003
from auth.application.ports.pwd_manager import IPasswordManager
from auth.application.ports.repo import AuthReader, AuthRepo, VerifyCodeRepo
from auth.infrastructure.adapters.jwt_manager import PyJWTManager
from auth.infrastructure.adapters.pwd_manager import PasswordManager
from common.application.ports.email_sender import IEmailSender
from config import Settings
from tests.mocks.auth import MockAuthRepo, MockEmailSender, MockVerifyCodeRepo
from tests.mocks.users import MockUserRepo
from users.application.ports.repo import UserReader, UserRepo


class MockAuthProvider(Provider):
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

    @provide
    def provide_auth_repo(self) -> Iterable[AuthRepo]:
        repo = MockAuthRepo()
        yield repo
        repo.user_tokens.clear()

    @provide
    def provide_auth_reader(self) -> Iterable[AuthReader]:
        repo = MockAuthRepo()
        yield repo
        repo.user_tokens.clear()

    @provide
    def provide_code_repo(self) -> Iterable[VerifyCodeRepo]:
        repo = MockVerifyCodeRepo()
        yield repo
        repo.verify_codes.clear()

    @provide
    def provide_user_reader(self) -> Iterable[UserReader]:
        repo = MockUserRepo()
        yield repo
        repo.users.clear()

    @provide
    def provide_user_repo(self) -> Iterable[UserRepo]:
        repo = MockUserRepo()
        yield repo
        repo.users.clear()

    email_sender = provide(MockEmailSender, provides=IEmailSender)
    pwd_manager = provide(PasswordManager, provides=IPasswordManager)

    login_handler = provide(LoginHandler)
    signup_handler = provide(SignUpHandler)
    signup_email_send = provide(SignUpEmailHandler)
    reset_email_send = provide(ResetEmailHandler)
    verify_email = provide(VerifyEmailHandler)
    reset_password = provide(ResetPasswordHandler)
    forget_password = provide(ForgetPasswordHandler)
    refresh_token = provide(RefreshHandler)
    logout_handler = provide(LogoutHandler)
