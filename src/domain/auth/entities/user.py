from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4

from domain.auth.enums.gender import Gender
from domain.auth.value_objects.email import Email
from domain.auth.value_objects.nickname import Nickname
from domain.auth.value_objects.password import Password
from domain.common.entities.entity import Entity


@dataclass(slots=True)
class User(Entity):
    password: Password
    email: Email
    nickname: Nickname
    gender: Gender = Gender.OTHER
    name: str | None = None
    lastname: str | None = None
    patronymic: str | None = None
    date_birth: date | None = None
    image: str | None = None
    id: UUID = field(default_factory=uuid4)
