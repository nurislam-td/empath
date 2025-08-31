from typing import Unpack, cast

import pytest
from dishka import AsyncContainer
from mimesis import Field, Generic, Locale, Schema

from auth.application.commands.signup import SignUp, SignUpHandler
from auth.application.ports.repo import AuthReader
from users.application.ports.repo import UserReader
from users.domain.value_objects.email import MismatchEmailError
from users.domain.value_objects.nickname import TooLongNicknameError
from users.domain.value_objects.password import MismatchPasswordError

from .protocols import UserData, UserDataFactory, UserDataKwargs


@pytest.fixture
def user_data_factory(generic_generator: Generic) -> UserDataFactory:
    field = Field(Locale.RU)

    def factory(**kwargs: Unpack[UserDataKwargs]) -> UserData:
        schema = Schema(
            lambda: {
                "email": field("person.email"),
                "password": generic_generator.password.secure(),
                "nickname": field("person.name"),
            },
            iterations=1,
        )
        return cast("UserData", {**schema.create()[0]} | {**kwargs})

    return factory


@pytest.fixture
def user_data(user_data_factory: UserDataFactory) -> UserData:
    return user_data_factory()


@pytest.fixture
async def signup_handler(request_container: AsyncContainer) -> SignUpHandler:
    return await request_container.get(SignUpHandler)


async def test_signup(
    request_container: AsyncContainer,
    user_data: UserData,
    signup_handler: SignUpHandler,
) -> None:
    await signup_handler(
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


@pytest.mark.parametrize(
    ("fields", "exc"),
    [
        ({"email": "invalid_email"}, MismatchEmailError),
        ({"password": "short"}, MismatchPasswordError),
        ({"nickname": "a" * 52}, TooLongNicknameError),
    ],
)
async def test_signup_validations(
    fields: UserDataKwargs,
    exc: type[Exception],
    user_data_factory: UserDataFactory,
    signup_handler: SignUpHandler,
) -> None:
    user_data = user_data_factory(**fields)

    with pytest.raises(exc):
        await signup_handler(
            SignUp(
                email=user_data["email"],
                password=user_data["password"],
                nickname=user_data["nickname"],
            ),
        )
