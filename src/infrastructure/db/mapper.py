from typing import Any

from sqlalchemy import RowMapping

from src.domain.auth import entities
from src.domain.auth import value_objects as vo


def convert_user_entity_to_db_model(user: entities.User) -> dict[str, Any]:
    return dict(
        id=user.id,
        nickname=user.nickname.to_base(),
        email=user.email.to_base(),
        password=user.password,
        lastname=user.lastname,
        name=user.name,
        patronymic=user.patronymic,
        date_birth=user.date_birth,
        gender=user.gender,
        image=user.image,
    )


def convert_db_model_to_user_entity(user: RowMapping) -> entities.User:
    return entities.User(
        id=user.id,
        nickname=vo.Nickname(user.nickname),
        email=vo.Email(user.email),
        password=user.password,
        lastname=user.lastname,
        name=user.name,
        patronymic=user.patronymic,
        date_birth=user.date_birth,
        gender=user.gender,
        image=user.image,
    )
