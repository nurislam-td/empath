from datetime import date

from common.api.schemas import BaseStruct, CamelizedBaseStruct
from users.domain.enums.gender import Gender


class UserUpdateSchema(BaseStruct):
    nickname: str
    gender: Gender
    name: str | None = None
    lastname: str | None = None
    patronymic: str | None = None
    date_birth: date | None = None


class UserUpdateFullnameSchema(BaseStruct):
    name: str
    lastname: str
    patronymic: str


class UpdateAvatarResponse(CamelizedBaseStruct):
    url: str
