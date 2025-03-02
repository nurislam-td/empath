from dataclasses import dataclass

from domain.common.exceptions import ValueObjectError
from domain.common.value_object import ValueObject


@dataclass(eq=False, slots=True)
class TooLongArticleTitleError(ValueObjectError):
    title: str

    @property
    def message(self):
        return f"Title too long: `{self.title}`"


@dataclass(frozen=True, slots=True)
class ArticleTitle(ValueObject[str]):
    def _validate(self):
        if len(self.value) > 50:
            raise TooLongArticleTitleError(self.value)
