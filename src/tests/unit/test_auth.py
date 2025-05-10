import random
import string
from collections.abc import Callable
from typing import Protocol, TypedDict, Unpack

import pytest
from dishka import AsyncContainer
from mimesis import Field, Generic, Locale, Schema
from mimesis.providers import BaseProvider

from auth.application.commands.signup import SignUp, SignUpHandler
from auth.application.ports.repo import AuthReader
from users.application.ports.repo import UserReader


class PasswordProvider(BaseProvider):
    class Meta:
        name = "password"

    def secure(self, length: int = 8) -> str:
        categories = [
            string.ascii_uppercase,
            string.ascii_lowercase,
            string.digits,
            "!@#$%^&*",
        ]
        password_chars = [random.choice(cat) for cat in categories]  # noqa: S311

        all_chars = string.ascii_letters + string.digits + "!@#$%^&*"
        remaining = length - len(password_chars)
        password_chars += [random.choice(all_chars) for _ in range(remaining)]  # noqa: S311

        random.shuffle(password_chars)
        return "".join(password_chars)


generic = Generic(Locale.RU)
generic.add_provider(PasswordProvider)


class TypedUserData(TypedDict):
    email: str
    password: str
    nickname: str


class TypedUserDataFactory(Protocol):
    def __call__(
        self,
        **fields: Unpack[TypedUserData],
    ) -> TypedUserData: ...


@pytest.fixture
def user_data_factory() -> TypedUserDataFactory:
    field = Field(Locale.RU)

    def factory(**fields: Unpack[TypedUserData]) -> TypedUserData:
        schema = Schema(
            lambda: {
                "email": field("person.email"),
                "password": generic.password.secure(),
                "nickname": field("person.name"),
            },
            iterations=1,
        )
        return TypedUserData(**schema.create()[0], **fields)

    return factory


@pytest.fixture
def user_data(user_data_factory: Callable[[], TypedUserData]) -> TypedUserData:
    return user_data_factory()


async def test_signup(
    request_container: AsyncContainer,
    user_data: TypedUserData,
) -> None:
    handler = await request_container.get(SignUpHandler)

    await handler(
        SignUp(
            email=user_data["email"],
            password=user_data["password"],
            nickname=user_data["nickname"],
        ),
    )

    token_repo = await request_container.get(AuthReader)
    user_repo = await request_container.get(UserReader)
    user = await user_repo.get_user_by_email(user_data["email"])
    assert user
    assert await token_repo.get_refresh_token(user.id)
