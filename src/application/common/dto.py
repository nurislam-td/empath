from dataclasses import asdict, dataclass, field
from typing import Any

from domain.common.constants import Empty


@dataclass(frozen=True, slots=True)
class DTO:
    def to_dict(self, exclude_unset: bool = False) -> dict[str, Any]:
        return {attr: value for attr, value in asdict(self).items() if (not exclude_unset or value is not Empty.UNSET)}


@dataclass
class PaginatedDTO[T: DTO]:
    count: int
    page: int
    next: int | None = field(init=False, default=None)
    prev: int | None = field(init=False, default=None)
    results: list[T] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.page < self.count:
            self.next = self.page + 1
        if self.page > 1:
            self.prev = self.page - 1
