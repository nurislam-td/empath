from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass(frozen=True, slots=True)
class UserDTO:
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
