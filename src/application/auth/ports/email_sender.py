from typing import Protocol


class IEmailSender(Protocol):
    def send_email(self, message: str): ...
