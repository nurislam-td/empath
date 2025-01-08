from dataclasses import dataclass

from application.auth.ports.pwd_manager import IPasswordManager
from application.auth.ports.repo import AuthReader, VerifyCodeRepo
from application.common.command import Command, CommandHandler
from application.common.ports.email_sender import IEmailSender


@dataclass(slots=True, frozen=True)
class ResetEmail(Command[None]):
    email: str


class ResetEmailHandler(CommandHandler[ResetEmail, None]):
    def __init__(
        self,
        email_client: IEmailSender,
        pwd_manager: IPasswordManager,
        auth_reader: AuthReader,
        verify_code_repo: VerifyCodeRepo,
    ) -> None:
        self._email_client = email_client
        self._password_manager = pwd_manager
        self._auth_reader = auth_reader
        self._verify_repo = verify_code_repo

    async def __call__(self, command: ResetEmail):
        await self._auth_reader.get_user_by_email(email=command.email)
        verify_code = self._password_manager.get_random_num()
        await self._verify_repo.set_verify_code(email=command.email, code=verify_code)
        self._email_client.send_email_template(
            emails=[command.email],
            template_name="verify_code_template",
            code=verify_code,
        )
