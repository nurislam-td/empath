from typing import Any

from sqlalchemy import RowMapping

from application.users.dto.user import UserDTO
from domain.users import entities
from domain.users import value_objects as vo


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


def convert_user_entity_to_user_dto(user: entities.User) -> UserDTO:
    return UserDTO(
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


def convert_db_model_to_dto(user: RowMapping) -> UserDTO:
    return UserDTO(
        id=user.id,
        nickname=user.nickname,
        email=user.email,
        password=user.password,
        lastname=user.lastname,
        name=user.name,
        patronymic=user.patronymic,
        date_birth=user.date_birth,
        gender=user.gender,
        image=user.image,
    )
