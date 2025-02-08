import re
from dataclasses import dataclass

from domain.common.exceptions import ValueObjectError
from domain.common.value_object.base import ValueObject

STRONG_PASSWORD_PATTERN = re.compile(
    r"(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{6,128}"
)


@dataclass(eq=False, slots=True)
class MismatchPasswordError(ValueObjectError):
    password: str

    @property
    def message(self):
        return f"Mismatch pattern: password must contain at least one lower character, one upper character, digit and special symbol: `{self.password}` ."


@dataclass(frozen=True, slots=True)
class Password(ValueObject[str]):
    def _validate(self):
        if not re.match(STRONG_PASSWORD_PATTERN, self.value):
            raise MismatchPasswordError(self.value)
