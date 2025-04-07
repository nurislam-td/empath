from dishka import Provider, Scope, provide  # type: ignore  # noqa: PGH003

from job.employment.application.commands.create_cv import CreateCVHandler
from job.employment.application.commands.response_to_vacancy import ResponseToVacancyHandler
from job.employment.application.commands.update_cv import UpdateCVHandler
from job.employment.application.queries.get_vacancies import GetVacanciesHandler
from job.employment.infrastructure.dao.employment_type import EmploymentTypeDAO
from job.employment.infrastructure.dao.rel_additional_skill_cv import RelCVAdditionalSkillDAO
from job.employment.infrastructure.dao.rel_skill_cv import RelCVSkillDAO
from job.employment.infrastructure.dao.skill import SkillDAO
from job.employment.infrastructure.dao.work_exp import WorkExpDAO
from job.employment.infrastructure.dao.work_format import WorkFormatDAO
from job.employment.infrastructure.dao.work_schedule import WorkScheduleDAO
from job.employment.infrastructure.repositories.cv import AlchemyCVRepo
from job.employment.infrastructure.repositories.response_to_vacancy import AlchemyVacancyResponseRepo
from job.employment.infrastructure.repositories.vacancy import AlchemyEmploymentVacancyReader


class EmploymentProvider(Provider):
    scope = Scope.REQUEST

    cv_repo = provide(AlchemyCVRepo)
    vacancy_response_repo = provide(AlchemyVacancyResponseRepo)
    vacancy_reader = provide(AlchemyEmploymentVacancyReader)

    work_exp = provide(WorkExpDAO)
    employment_type = provide(EmploymentTypeDAO)
    skill = provide(SkillDAO)
    work_format = provide(WorkFormatDAO)
    work_schedule = provide(WorkScheduleDAO)
    rel_additional_skill_vacancy = provide(RelCVAdditionalSkillDAO)
    rel_skill_vacancy = provide(RelCVSkillDAO)

    create_cv = provide(CreateCVHandler)
    update_cv = provide(UpdateCVHandler)
    response_to_vacancy = provide(ResponseToVacancyHandler)

    get_vacancies = provide(GetVacanciesHandler)
