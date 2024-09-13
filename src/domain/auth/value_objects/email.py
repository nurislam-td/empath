import re
from dataclasses import dataclass

from domain.common.exceptions import ValueObjectError
from domain.common.value_object.base import ValueObject

EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")


@dataclass(eq=False, slots=True)
class MismatchEmailError(ValueObjectError):
    email: str

    @property
    def message(self):
        return f"Invalid email:{self.email}"


@dataclass(frozen=True, slots=True)
class Email(ValueObject[str]):
    def _validate(self):
        if not re.match(EMAIL_PATTERN, self.value):
            raise MismatchEmailError(self.value)
