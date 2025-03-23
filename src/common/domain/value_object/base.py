from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValueObject[T](ABC):
    value: T

    @abstractmethod
    def _validate(self) -> None: ...

    def __post_init__(self) -> None:
        self._validate()

    def to_base(self) -> T:
        return self.value
