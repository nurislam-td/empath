from dataclasses import dataclass
from uuid import UUID

from application.common.exceptions import ApplicationError


@dataclass(slots=True, eq=False)
class EmptyArticleUpdatesError(ApplicationError):
    @property
    def message(self) -> str:
        return "At least one field must be filled in for editing."


@dataclass(slots=True, eq=False)
class ArticleIdNotExistError(ApplicationError):
    article_id: UUID

    @property
    def message(self) -> str:
        return f"Article with that id not exist: {self.article_id}"
