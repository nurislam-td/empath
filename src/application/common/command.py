from abc import ABC
from typing import Protocol


class Command(ABC):
    pass


class CommandHandler[C: Command, CRes](Protocol):
    async def __call__(self, command: C) -> CRes: ...
