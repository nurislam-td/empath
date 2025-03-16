from dataclasses import dataclass
from uuid import UUID

from application.common.exceptions import ApplicationError


@dataclass(slots=True, eq=False)
class UserEmailNotExistError(ApplicationError):
    email: str

    @property
    def message(self):
        return f"User with that email not exist: {self.email}"


@dataclass(slots=True, eq=False)
class UserIdNotExistError(ApplicationError):
    user_id: UUID

    @property
    def message(self):
        return f"User with that id not exist: {self.user_id}"


@dataclass(slots=True, eq=False)
class UserEmailAlreadyExistError(ApplicationError):
    email: str

    @property
    def message(self):
        return f"User with that email already exist: {self.email}"
