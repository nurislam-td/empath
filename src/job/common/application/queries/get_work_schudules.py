from dataclasses import dataclass

from job.common.application.ports.repo import VacancyReader
from job.recruitment.application.dto import WorkScheduleDTO


@dataclass(frozen=True, slots=True)
class GetWorkSchedulesHandler:
    _reader: VacancyReader

    async def __call__(self) -> list[WorkScheduleDTO]:
        return await self._reader.get_work_schedules()
