from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class Event:
    event_id: UUID = field(init=False, kw_only=True, default_factory=uuid4)
    event_timestamp: datetime = field(
        init=False, kw_only=True, default_factory=lambda: datetime.now(timezone.utc)
    )
