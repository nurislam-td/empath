from dataclasses import dataclass

from auth.application.const import VERIFY_CODE_SEND_TEMPLATE_PATH
from auth.application.ports.pwd_manager import IPasswordManager
from auth.application.ports.repo import VerifyCodeRepo
from common.application.command import Command, CommandHandler
from common.application.ports.email_sender import IEmailSender
from users.application.exceptions import UserEmailAlreadyExistError
from users.application.ports.repo import UserReader
from users.domain.value_objects.email import Email


@dataclass(slots=True, frozen=True)
class SignUpEmail(Command[None]):
    email: str


class SignUpEmailHandler(CommandHandler[SignUpEmail, None]):
    def __init__(
        self,
        email_client: IEmailSender,
        pwd_manager: IPasswordManager,
        verify_code_repo: VerifyCodeRepo,
        user_reader: UserReader,
    ) -> None:
        self._email_client = email_client
        self._password_manager = pwd_manager
        self._verify_repo = verify_code_repo
        self._user_reader = user_reader

    async def __call__(self, command: SignUpEmail):
        if await self._user_reader.check_email_existence(email=Email(command.email).to_base()):
            raise UserEmailAlreadyExistError(email=command.email)
        verify_code = "718293"  # self._password_manager.get_random_num()
        await self._verify_repo.set_verify_code(email=command.email, code=verify_code)
        # self._email_client.send_email_template(
        #     emails=[command.email],
        #     template_name=VERIFY_CODE_SEND_TEMPLATE_PATH,
        #     code=verify_code,
        # )
