from dataclasses import dataclass

from application.auth.ports.pwd_manager import IPasswordManager
from application.auth.ports.repo import VerifyCodeRepo
from application.common.command import Command, CommandHandler
from application.common.ports.email_sender import IEmailSender


@dataclass(slots=True)
class RegistryEmail(Command[bool]):
    email: str


class RegistryEmailHandler(CommandHandler[RegistryEmail, bool]):
    def __init__(
        self,
        email_client: IEmailSender,
        pwd_manager: IPasswordManager,
        verify_code_repo: VerifyCodeRepo,
    ) -> None:
        self._email_client = email_client
        self._password_manager = pwd_manager
        self._verify_repo = verify_code_repo

    async def __call__(self, command: RegistryEmail):
        verify_code = self._password_manager.get_random_num()
        await self._verify_repo.set_verify_code(email=command.email, code=verify_code)
        self._email_client.send_email_template(
            emails=[command.email],
            template_name="verify_code_template",
            code=verify_code,
        )
