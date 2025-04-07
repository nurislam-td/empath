from dishka import Provider, Scope, provide  # type: ignore  # noqa: PGH003

from job.common.application.ports.repo import VacancyReader
from job.common.application.queries.get_cv_by_id import GetCVByIdHandler
from job.common.application.queries.get_employment_types import GetEmploymentTypesHandler
from job.common.application.queries.get_skills import GetSkillsHandler
from job.common.application.queries.get_vacancies import GetVacanciesHandler
from job.common.application.queries.get_vacancy_by_id import GetVacancyByIdHandler
from job.common.application.queries.get_vacancy_responses import GetVacancyResponsesHandler
from job.common.application.queries.get_work_formats import GetWorkFormatsHandler
from job.common.application.queries.get_work_schedules import GetWorkSchedulesHandler
from job.common.infrastructure.repositories.cv import AlchemyCVReader
from job.common.infrastructure.repositories.vacancy import AlchemyVacancyReader
from job.common.infrastructure.repositories.vacancy_responses import AlchemyVacancyResponseReader


class JobProvider(Provider):
    scope = Scope.REQUEST

    vacancy_reader = provide(AlchemyVacancyReader, provides=VacancyReader)
    cv_reader = provide(AlchemyCVReader)
    vacancy_response_reader = provide(AlchemyVacancyResponseReader)

    get_vacancies = provide(GetVacanciesHandler)
    get_vacancy_by_id = provide(GetVacancyByIdHandler)
    get_skills = provide(GetSkillsHandler)
    get_work_schedules = provide(GetWorkSchedulesHandler)
    get_employment_types = provide(GetEmploymentTypesHandler)
    get_work_formats = provide(GetWorkFormatsHandler)
    get_cv_by_id = provide(GetCVByIdHandler)
    get_vacancy_responses = provide(GetVacancyResponsesHandler)
