from dataclasses import dataclass

from application.auth.ports.repo import AuthReader
from application.common.command import Command, CommandHandler


@dataclass(slots=True)
class VerifyEmail(Command[bool]):
    email: str
    code: str


class VerifyEmailHandler(CommandHandler[VerifyEmail, bool]):
    def __init__(self, auth_reader: AuthReader):
        self._auth_reader = auth_reader

    async def __call__(self, command: VerifyEmail):
        code = await self._auth_reader.get_user_code_by_email(command.email)
        return code == command.code
