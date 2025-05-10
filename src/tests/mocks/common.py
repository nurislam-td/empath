from common.application.uow import UnitOfWork


class MockUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.commit_called = False
        self.rollback_called = False

    async def commit(self) -> None:
        self.commit_called = True

    async def rollback(self) -> None:
        self.rollback_called = True
