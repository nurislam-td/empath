from abc import ABC
from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True)
class Entity(ABC):
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
