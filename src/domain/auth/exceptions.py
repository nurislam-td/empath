from dataclasses import dataclass

from domain.common.exceptions import ValueObjectError


@dataclass(eq=False, slots=True)
class MismatchPasswordError(ValueObjectError):
    password: str

    @property
    def message(self):
        return f"Mismatch pattern: password must contain at least one lower character, one upper character, digit and special symbol, {self.password}."


@dataclass(eq=False, slots=True)
class MismatchEmailError(ValueObjectError):
    email: str

    @property
    def message(self):
        return f"Invalid email:{self.email}"


@dataclass(eq=False, slots=True)
class TooLongNicknameError(ValueObjectError):
    nickname: str

    @property
    def message(self):
        return f"Nickname too long: {self.nickname}"
