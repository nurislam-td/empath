from abc import ABC, abstractmethod
from typing import Generic, TypeVar

QRes = TypeVar("QRes")


class Query(ABC, Generic[QRes]):
    pass


Q = TypeVar("Q", bound=Query)  # type: ignore


class QueryHandler(ABC, Generic[Q, QRes]):
    @abstractmethod
    async def __call__(self, query: Q) -> QRes: ...
