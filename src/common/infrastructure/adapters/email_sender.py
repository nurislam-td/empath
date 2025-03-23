from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from ssl import create_default_context
from typing import Any

from common.application.ports.email_sender import IEmailSender
from common.infrastructure.adapters import render
from config import get_settings

settings = get_settings().email


class EmailSender(IEmailSender):
    def send_email_template(self, emails: list[str], template_name: str, **data: Any) -> str | dict[str, Any]:  # noqa: ANN401
        template = render.render_template(template_name, **data)

        message = MIMEMultipart("alternative")
        message["From"] = settings.MAIL_USERNAME
        message["To"] = ",".join(emails)
        message["Subject"] = "Empath notification"
        message.attach(MIMEText(template, "html"))
        ctx = create_default_context()
        try:
            with SMTP(settings.MAIL_HOST, settings.MAIL_PORT) as server:
                server.ehlo()
                server.starttls(context=ctx)
                server.ehlo()
                server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
                server.sendmail(
                    from_addr=message["From"],
                    to_addrs=message["To"],
                    msg=message.as_string(),
                )
                server.quit()
            return message.as_string()
        except Exception as e:  # noqa: BLE001
            return {"error": e}
