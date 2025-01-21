from dataclasses import dataclass

from application.auth.const import VERIFY_CODE_SEND_TEMPLATE_PATH
from application.auth.ports.pwd_manager import IPasswordManager
from application.auth.ports.repo import VerifyCodeRepo
from application.common.command import Command, CommandHandler
from application.common.ports.email_sender import IEmailSender
from application.users.ports.repo import UserReader


@dataclass(slots=True, frozen=True)
class ResetEmail(Command[None]):
    email: str


class ResetEmailHandler(CommandHandler[ResetEmail, None]):
    def __init__(
        self,
        email_client: IEmailSender,
        pwd_manager: IPasswordManager,
        user_reader: UserReader,
        verify_code_repo: VerifyCodeRepo,
    ) -> None:
        self._email_client = email_client
        self._password_manager = pwd_manager
        self._user_reader = user_reader
        self._verify_repo = verify_code_repo

    async def __call__(self, command: ResetEmail):
        await self._user_reader.get_user_by_email(email=command.email)
        verify_code = self._password_manager.get_random_num()
        await self._verify_repo.set_verify_code(email=command.email, code=verify_code)
        self._email_client.send_email_template(
            emails=[command.email],
            template_name=VERIFY_CODE_SEND_TEMPLATE_PATH,
            code=verify_code,
        )
