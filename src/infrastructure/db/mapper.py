from typing import Any

from src.domain.auth import entities


def convert_user_entity_to_db_model(user: entities.User) -> dict[str, Any]:
    return dict(
        id=user.id,
        nickname=user.nickname.to_base(),
        email=user.email.to_base(),
        password=user.password.to_base().encode(),
        lastname=user.lastname,
        name=user.name,
        patronymic=user.patronymic,
        date_birth=user.date_birth,
        gender=user.gender,
        image=user.image,
    )
