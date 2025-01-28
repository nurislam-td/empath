from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class DTO:
    pass


@dataclass
class PaginatedDTO[T: DTO]:
    count: int
    page: int
    next: int | None = field(init=False, default=None)
    prev: int | None = field(init=False, default=None)
    results: list[T] = field(default_factory=list)

    def __post_init__(self):
        if self.page < self.count:
            self.next = self.page + 1
        if self.page > 1:
            self.prev = self.page - 1
