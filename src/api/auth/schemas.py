from infrastructure.common.schemas import CamelizedBaseStruct


class LoginSchema(CamelizedBaseStruct):
    email: str
    password: str


class SignUpSchema(LoginSchema):
    nickname: str
