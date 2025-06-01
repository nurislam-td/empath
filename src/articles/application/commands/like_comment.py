from dataclasses import dataclass
from uuid import UUID

from articles.application.exceptions import NothingToCancelError
from articles.application.ports.repo import CommentReader, CommentRepo
from common.application.command import Command, CommandHandler
from common.application.uow import UnitOfWork
from users.application.ports.repo import UserReader, UserRepo


@dataclass(frozen=True, slots=True)
class LikeComment(Command[None]):
    id: UUID
    user_id: UUID


@dataclass
class LikeCommentHandler(CommandHandler[LikeComment, None]):
    _comment_repo: CommentRepo
    _comment_reader: CommentReader
    _user_reader: UserReader
    _user_repo: UserRepo
    _uow: UnitOfWork

    async def __call__(self, command: LikeComment) -> None:
        comment = await self._comment_reader.get_comment_by_id(comment_id=command.id, user_id=command.user_id)
        plus_rating = 1

        try:
            await self._comment_repo.cancel_dislike_comment(comment_id=command.id, user_id=command.user_id)
        except NothingToCancelError:
            pass
        else:
            plus_rating += 1

        await self._comment_repo.like_comment(comment_id=command.id, user_id=command.user_id)
        user = await self._user_reader.get_user_by_id(comment.author.id)
        await self._user_repo.update_user({"rating": user.rating + plus_rating}, {"id": user.id})
        await self._uow.commit()
