from uuid import UUID

from common.api.schemas import BaseStruct, CamelizedBaseStruct


class LoginSchema(CamelizedBaseStruct):
    email: str = "string@email.com"
    password: str = "String03@"  # noqa: S105


class SignUpSchema(LoginSchema):
    nickname: str = "string"


class JWTUserPayload(BaseStruct):
    sub: UUID
    email: str


class ResetPasswordSchema(CamelizedBaseStruct):
    old_password: str
    new_password: str


class ForgetPasswordSchema(LoginSchema):
    pass


class RefreshTokenSchema(CamelizedBaseStruct):
    refresh_token: str
