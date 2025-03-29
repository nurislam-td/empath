from dataclasses import dataclass
from uuid import UUID

from articles.application.ports.repo import CommentRepo
from common.application.command import Command, CommandHandler
from common.application.uow import UnitOfWork


@dataclass(slots=True, frozen=True)
class DeleteComment(Command[None]):
    comment_id: UUID


@dataclass(slots=True, frozen=True)
class DeleteCommentHandler(CommandHandler[DeleteComment, None]):
    _repo: CommentRepo
    _uow: UnitOfWork

    async def __call__(self, command: DeleteComment) -> None:
        await self._repo.delete_comment(command.comment_id)
        await self._uow.commit()
