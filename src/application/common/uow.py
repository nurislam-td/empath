from typing import Protocol


class UnitOfWork(Protocol):
    async def commit(self): ...

    async def rollback(self): ...
