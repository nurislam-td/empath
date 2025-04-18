from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4

from common.domain.entities import Entity
from users.domain.enums.gender import Gender
from users.domain.value_objects.email import Email
from users.domain.value_objects.nickname import Nickname


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
    rating: int = field(default=0)
    id: UUID = field(default_factory=uuid4)
