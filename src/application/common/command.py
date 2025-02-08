from abc import ABC, abstractmethod
from typing import Generic, TypeVar

CRes = TypeVar("CRes")


class Command(ABC, Generic[CRes]):
    pass


C = TypeVar("C", bound=Command)  # type: ignore


class CommandHandler(Generic[C, CRes], ABC):
    @abstractmethod
    async def __call__(self, command: C) -> CRes: ...
