from datetime import date

from domain.users.enums.gender import Gender
from infrastructure.common.schemas import CamelizedBaseStruct


class UserUpdateSchema(CamelizedBaseStruct):
    nickname: str
    gender: Gender
    name: str | None = None
    lastname: str | None = None
    patronymic: str | None = None
    date_birth: date | None = None
