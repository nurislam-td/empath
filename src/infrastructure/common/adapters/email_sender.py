from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from ssl import create_default_context
from typing import Any

from application.common.ports.email_sender import IEmailSender
from infrastructure.common.adapters import render


class EmailSender(IEmailSender):
    def send_email_template(
        self, emails: list[str], template_name: str, **data
    ) -> str | dict[str, Any]:
        template = render.render_template(template_name, **data)

        message = MIMEMultipart("alternative")
        message["From"] = MAIL_USERNAME
        message["To"] = ",".join(emails)
        message["Subject"] = "Empath notification"
        message.attach(MIMEText(template, "html"))
        ctx = create_default_context()
        try:
            with SMTP(MAIL_HOST, MAIL_PORT) as server:
                server.ehlo()
                server.starttls(context=ctx)
                server.ehlo()
                server.login(MAIL_USERNAME, MAIL_PASSWORD)
                server.sendmail(
                    from_addr=message["From"],
                    to_addrs=message["To"],
                    msg=message.as_string(),
                )
                server.quit()
            return message.as_string()
        except Exception as e:
            return {"error": e}
