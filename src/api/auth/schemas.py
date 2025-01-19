from uuid import UUID

from infrastructure.common.schemas import BaseStruct, CamelizedBaseStruct


class LoginSchema(CamelizedBaseStruct):
    email: str
    password: str


class SignUpSchema(LoginSchema):
    nickname: str


class JWTUserPayload(BaseStruct):
    sub: UUID
    email: str


class ResetPasswordSchema(CamelizedBaseStruct):
    old_password: str
    new_password: str


class ForgetPasswordSchema(LoginSchema):
    pass
