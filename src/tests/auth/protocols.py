from typing import NotRequired, Protocol, TypedDict, Unpack


class UserDataKwargs(TypedDict):
    email: NotRequired[str]
    password: NotRequired[str]
    nickname: NotRequired[str]


class UserData(TypedDict):
    email: str
    password: str
    nickname: str


class UserDataFactory(Protocol):
    def __call__(
        self,
        **kwargs: Unpack[UserDataKwargs],
    ) -> UserData: ...
