from dataclasses import dataclass

from common.domain.exceptions import ValueObjectError
from common.domain.value_object.base import ValueObject

NICKNAME_LEN = 12


@dataclass(eq=False, slots=True)
class TooLongNicknameError(ValueObjectError):
    nickname: str

    @property
    def message(self) -> str:
        return f"Nickname too long: `{self.nickname}`"


@dataclass(frozen=True, slots=True)
class Nickname(ValueObject[str]):
    def _validate(self) -> None:
        if len(self.value) > NICKNAME_LEN:
            raise TooLongNicknameError(self.value)
