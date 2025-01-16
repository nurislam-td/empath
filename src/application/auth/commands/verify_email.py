from dataclasses import dataclass

from application.auth.ports.repo import VerifyCodeRepo
from application.common.command import Command, CommandHandler


@dataclass(slots=True)
class VerifyEmail(Command[bool]):
    email: str
    code: str


class VerifyEmailHandler(CommandHandler[VerifyEmail, bool]):
    def __init__(self, verify_code_repo: VerifyCodeRepo):
        self._repo = verify_code_repo

    async def __call__(self, command: VerifyEmail):
        code = await self._repo.get_verify_code(command.email)
        if code != command.code:
            raise Exception("Code not correct")
        return code == command.code
