from dataclasses import dataclass
from uuid import UUID

from articles.application.ports.repo import CommentReader, CommentRepo
from common.application.command import Command, CommandHandler
from common.application.uow import UnitOfWork
from users.application.ports.repo import UserReader, UserRepo


@dataclass(frozen=True, slots=True)
class DislikeComment(Command[None]):
    id: UUID
    user_id: UUID


@dataclass
class DislikeCommentHandler(CommandHandler[DislikeComment, None]):
    _comment_repo: CommentRepo
    _comment_reader: CommentReader
    _user_reader: UserReader
    _user_repo: UserRepo
    _uow: UnitOfWork

    async def __call__(self, command: DislikeComment) -> None:
        comment = await self._comment_reader.get_comment_by_id(command.id)
        await self._comment_repo.dislike_comment(comment_id=command.id, user_id=command.user_id)
        user = await self._user_reader.get_user_by_id(comment.author.id)
        await self._user_repo.update_user({"rating": user.rating - 1}, {"id": user.id})
        await self._uow.commit()
