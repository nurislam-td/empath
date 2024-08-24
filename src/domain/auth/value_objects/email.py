import re
from dataclasses import dataclass

from domain.auth.exceptions import MismatchEmailError
from domain.common.value_object.base import ValueObject

EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")


@dataclass(frozen=True, slots=True)
class Email(ValueObject[str]):
    def _validate(self):
        if not re.match(EMAIL_PATTERN, self.value):
            raise MismatchEmailError(self.value)
