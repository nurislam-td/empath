from dataclasses import dataclass
from uuid import UUID

from articles.application.exceptions import ContentAuthorMismatchError
from articles.application.ports.repo import CommentReader, CommentRepo
from common.application.command import Command, CommandHandler
from common.application.uow import UnitOfWork


@dataclass(frozen=True, slots=True)
class EditComment(Command[None]):
    id: UUID
    author_id: UUID
    article_id: UUID
    text: str


@dataclass(slots=True)
class EditCommentHandler(CommandHandler[EditComment, None]):
    _repo: CommentRepo
    _reader: CommentReader
    _uow: UnitOfWork

    async def __call__(self, command: EditComment) -> None:
        comment_dto = await self._reader.get_comment_by_id(command.id)
        if comment_dto.author.id != command.author_id:
            raise ContentAuthorMismatchError
        await self._repo.update_comment(command)
        await self._uow.commit()
