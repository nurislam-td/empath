from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4

from domain.common.entities.entity import Entity
from domain.users.enums.gender import Gender
from domain.users.value_objects.email import Email
from domain.users.value_objects.nickname import Nickname


@dataclass(slots=True)
class User(Entity):
    password: bytes
    email: Email
    nickname: Nickname
    gender: Gender = Gender.OTHER
    name: str | None = None
    lastname: str | None = None
    patronymic: str | None = None
    date_birth: date | None = None
    image: str | None = None
    id: UUID = field(default_factory=uuid4)
