from dataclasses import dataclass
from uuid import UUID

from common.application.dto import DTO


@dataclass(frozen=True, slots=True)
class WorkFormatDTO(DTO):
    name: str
    id: UUID


@dataclass(frozen=True, slots=True)
class SalaryDTO(DTO):
    from_: int
    to: int


@dataclass(frozen=True, slots=True)
class EmploymentTypeDTO(DTO):
    name: str
    id: UUID


@dataclass(frozen=True, slots=True)
class WorkScheduleDTO(DTO):
    name: str
    id: UUID


@dataclass(frozen=True, slots=True)
class SkillDTO(DTO):
    name: str
    id: UUID
