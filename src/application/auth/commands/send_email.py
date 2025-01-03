from dataclasses import dataclass

from application.auth.ports.email_sender import IEmailSender
from application.auth.ports.task_manager import ITaskManager
from application.common.command import Command, CommandHandler


@dataclass(slots=True)
class SendVerifyEmail(Command[bool]):
    email: str


class SendVerifyEmailHandler(CommandHandler[SendVerifyEmail, bool]):
    def __init__(self, email_client: IEmailSender, task_manager: ITaskManager) -> None:
        self._email_client = email_client
        self._task_manager = task_manager

    def __call__(self, command: SendVerifyEmail):
        self._task_manager.create_task(self._email_client.send_email(command.email))
