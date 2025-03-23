from dataclasses import dataclass

from articles.domain.constants import ARTICLE_TITLE_LEN
from common.domain.exceptions import ValueObjectError
from common.domain.value_object import ValueObject


@dataclass(eq=False, slots=True)
class TooLongArticleTitleError(ValueObjectError):
    title: str

    @property
    def message(self) -> str:
        return f"Title too long: `{self.title}`, max length is {ARTICLE_TITLE_LEN}"


@dataclass(frozen=True, slots=True)
class ArticleTitle(ValueObject[str]):
    def _validate(self) -> None:
        if len(self.value) > ARTICLE_TITLE_LEN:
            raise TooLongArticleTitleError(self.value)
