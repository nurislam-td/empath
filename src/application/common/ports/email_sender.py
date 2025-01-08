from typing import Any, Protocol


class IEmailSender(Protocol):
    def send_email_template(
        self, emails: list[str], template_name: str, **data
    ) -> str | dict[str, Any]: ...
