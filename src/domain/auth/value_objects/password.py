import re
from dataclasses import dataclass

from domain.auth.exceptions import MismatchPasswordError
from domain.common.value_object.base import ValueObject

STRONG_PASSWORD_PATTERN = re.compile(
    r"(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{6,128}"
)


@dataclass(frozen=True, slots=True)
class Password(ValueObject[str]):
    def _validate(self):
        if not re.match(STRONG_PASSWORD_PATTERN, self.value):
            raise MismatchPasswordError(self.value)
