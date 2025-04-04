from common.api.schemas import BaseStruct
from job.common.domain.enums import EducationEnum, WorkExpEnum, WorkFormatEnum


class GetVacanciesFilters(BaseStruct):
    salary_from: int | None = None
    salary_to: int | None = None
    work_exp: list[WorkExpEnum] | None = None
    education: list[EducationEnum] | None = None
    work_format: list[WorkFormatEnum] | None = None
    exclude_word: list[str] | None = None
    include_word: list[str] | None = None
    search: str | None = None
