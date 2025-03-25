from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from typing import Any, Generic, TypeVar

QRes = TypeVar("QRes")


@dataclass(frozen=True)
class Query(ABC, Generic[QRes]):
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


Q = TypeVar("Q", bound=Query)  # type: ignore


class QueryHandler(ABC, Generic[Q, QRes]):
    @abstractmethod
    async def __call__(self, query: Q) -> QRes: ...


@dataclass(frozen=True, slots=True)
class PaginationParams:
    page: int
    per_page: int = field(default=5)
