from dataclasses import dataclass

from domain.articles.constants import TAG_NAME_LEN
from domain.common.exceptions import ValueObjectError
from domain.common.value_object import ValueObject


@dataclass(eq=False, slots=True)
class TooLongTagNameError(ValueObjectError):
    name: str

    @property
    def message(self) -> str:
        return f"Tag name too long: `{self.name}`, max length is {TAG_NAME_LEN}"


@dataclass(frozen=True, slots=True)
class TagName(ValueObject[str]):
    def _validate(self) -> None:
        if len(self.value) > TAG_NAME_LEN:
            raise TooLongTagNameError(self.value)
