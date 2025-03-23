from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any, Generic, TypeVar

from common.domain.constants import Empty

CRes = TypeVar("CRes")


@dataclass(frozen=True, slots=True)
class Command(ABC, Generic[CRes]):
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_dict_exclude_unset(self) -> dict[str, Any]:
        return {attr: value for attr, value in asdict(self).items() if value is not Empty.UNSET}


C = TypeVar("C", bound=Command)  # type: ignore


class CommandHandler(Generic[C, CRes], ABC):
    @abstractmethod
    async def __call__(self, command: C) -> CRes: ...
