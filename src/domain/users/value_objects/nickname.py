from dataclasses import dataclass

from domain.common.exceptions import ValueObjectError
from domain.common.value_object.base import ValueObject


@dataclass(eq=False, slots=True)
class TooLongNicknameError(ValueObjectError):
    nickname: str

    @property
    def message(self):
        return f"Nickname too long: {self.nickname}"


@dataclass(frozen=True, slots=True)
class Nickname(ValueObject[str]):
    def _validate(self):
        if len(self.value) > 12:
            raise TooLongNicknameError(self.value)
