from dataclasses import dataclass

from domain.auth.exceptions import TooLongNicknameError
from domain.common.value_object.base import ValueObject


@dataclass(frozen=True, slots=True)
class Nickname(ValueObject[str]):
    def _validate(self):
        if len(self.value) > 12:
            raise TooLongNicknameError(self.value)
