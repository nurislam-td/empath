from dataclasses import dataclass, field
from uuid import UUID, uuid4

from articles.application.ports.repo import CommentRepo
from common.application.command import Command, CommandHandler
from common.application.uow import UnitOfWork


@dataclass(slots=True, frozen=True)
class CreateComment(Command[None]):
    text: str
    article_id: UUID
    author_id: UUID
    parent_id: UUID | None = None
    id: UUID = field(default_factory=uuid4)


@dataclass
class CreateCommentHandler(CommandHandler[CreateComment, None]):
    _repo: CommentRepo
    _uow: UnitOfWork

    async def __call__(self, command: CreateComment) -> None:
        await self._repo.create_comment(command)
        await self._uow.commit()
