from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValueObject[T](ABC):
    value: T

    @abstractmethod
    def _validate(self): ...

    def __post_init__(self):
        self._validate()

    def to_base(self) -> T:
        return self.value
