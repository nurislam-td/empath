from dataclasses import dataclass

from auth.application.exceptions import InvalidVerificationCodeError
from auth.application.ports.repo import VerifyCodeRepo
from common.application.command import Command, CommandHandler
from users.domain.value_objects.email import Email


@dataclass(slots=True, frozen=True)
class VerifyEmail(Command[bool]):
    email: str
    code: str


class VerifyEmailHandler(CommandHandler[VerifyEmail, bool]):
    def __init__(self, verify_code_repo: VerifyCodeRepo) -> None:
        self._repo = verify_code_repo

    async def __call__(self, command: VerifyEmail) -> bool:
        Email(command.email)
        code = await self._repo.get_verify_code(command.email)
        if code != command.code:
            raise InvalidVerificationCodeError
        return code == command.code
