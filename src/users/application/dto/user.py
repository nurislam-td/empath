from dataclasses import dataclass
from datetime import date
from uuid import UUID

from common.application.dto import DTO, PaginatedDTO


@dataclass(frozen=True, slots=True)
class UserDTO(DTO):
    id: UUID
    nickname: str
    email: str
    password: bytes
    lastname: str | None
    name: str | None
    patronymic: str | None
    date_birth: date | None
    gender: str | None
    image: str | None


type PaginatedUserDTO = PaginatedDTO[UserDTO]
