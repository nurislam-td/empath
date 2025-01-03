from dataclasses import dataclass
from typing import Protocol


@dataclass
class ITaskManager(Protocol):
    def create_task(self, task): ...
