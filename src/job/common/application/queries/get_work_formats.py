from dataclasses import dataclass

from job.common.infrastructure.repositories.vacancy import AlchemyVacancyReader
from job.recruitment.application.dto import WorkFormatDTO


@dataclass(frozen=True, slots=True)
class GetWorkFormatsHandler:
    _reader: AlchemyVacancyReader

    async def __call__(self) -> list[WorkFormatDTO]:
        return await self._reader.get_work_formats()
