from dataclasses import dataclass

from job.common.application.ports.repo import VacancyReader
from job.recruitment.application.dto import WorkFormatDTO


@dataclass(frozen=True, slots=True)
class GetWorkFormatsHandler:
    _reader: VacancyReader

    async def __call__(self) -> list[WorkFormatDTO]:
        return await self._reader.get_work_formats()
