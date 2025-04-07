from uuid import UUID, uuid4

from msgspec import field

from common.api.schemas import BaseStruct


class SkillSchema(BaseStruct):
    name: str
    id: UUID = field(default_factory=uuid4)


class SalarySchema(BaseStruct):
    from_: int = field(name="from")
    to: int | None = field(name="to", default=None)
