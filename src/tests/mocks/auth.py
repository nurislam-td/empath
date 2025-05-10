from datetime import UTC, datetime, timedelta
from typing import Any, ClassVar
from uuid import UUID

from auth.application.ports.repo import AuthReader, AuthRepo, VerifyCodeRepo
from auth.domain.value_objects.jwt import JWTPair
from common.application.ports.email_sender import IEmailSender


class MockAuthRepo(AuthRepo, AuthReader):
    user_tokens: ClassVar[dict[UUID, dict[str, str]]] = {}

    async def create_jwt(self, jwt: JWTPair, user_id: UUID) -> None:
        self.user_tokens[user_id] = {
            "access_token": jwt.access_token,
            "refresh_token": jwt.refresh_token,
        }

    async def refresh_jwt(self, jwt: JWTPair, user_id: UUID) -> None:
        self.user_tokens[user_id] = {
            "access_token": jwt.access_token,
            "refresh_token": jwt.refresh_token,
        }

    async def delete_refresh_jwt(self, user_id: UUID) -> None:
        self.user_tokens.pop(user_id, None)

    async def get_refresh_token(self, user_id: UUID) -> str:
        return self.user_tokens[user_id]["refresh_token"]


class MockVerifyCodeRepo(VerifyCodeRepo):
    verify_codes: ClassVar[dict[str, dict[str, Any]]] = {}

    async def set_verify_code(self, email: str, code: str, expires_in: int | timedelta | None = None) -> None:
        if isinstance(expires_in, timedelta):
            expires_in = int(expires_in.total_seconds())

        self.verify_codes[email] = {
            "code": code,
            "expired_at": datetime.now(UTC) + timedelta(seconds=expires_in) if expires_in else None,
        }

    async def get_verify_code(self, email: str) -> str | None:
        verify_code = self.verify_codes.get(email)
        if not verify_code:
            return None

        if (verify_code["expired_at"] is None) or (verify_code["expired_at"] > datetime.now(UTC)):
            return verify_code["code"]

        return None


class MockEmailSender(IEmailSender):
    def __init__(self) -> None:
        self.sended = False

    def send_email_template(
        self,
        emails: list[str],
        template_name: str,
        **data: Any,  # noqa: ANN401
    ) -> str | dict[str, Any]:
        self.sended = True
        return "ok"
