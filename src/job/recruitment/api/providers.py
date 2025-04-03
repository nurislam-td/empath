from dishka import Provider, Scope, provide  # type: ignore  # noqa: PGH003

from job.common.infrastructure.repositories.employment_type import EmploymentTypeDAO
from job.common.infrastructure.repositories.rel_additional_skill_vacancy import RelVacancyAdditionalSkillDAO
from job.common.infrastructure.repositories.rel_skill_vacancy import RelVacancySkillDAO
from job.common.infrastructure.repositories.skill import SkillDAO
from job.common.infrastructure.repositories.vacancy import AlchemyVacancyReader, AlchemyVacancyRepo
from job.common.infrastructure.repositories.work_schedule import WorkScheduleDAO
from job.recruitment.application.commands.create_vacancy import CreateVacancyHandler
from job.recruitment.application.commands.delete_vacancy import DeleteVacancyHandler
from job.recruitment.application.commands.edit_vacancy import UpdateVacancyHandler
from job.recruitment.application.queries.get_vacancies import GetVacanciesHandler


class RecruitmentProvider(Provider):
    scope = Scope.REQUEST

    vacancy_repo = provide(AlchemyVacancyRepo)
    vacancy_reader = provide(AlchemyVacancyReader)

    rel_additional_skill_vacancy = provide(RelVacancyAdditionalSkillDAO)  # TODO split this
    rel_skill_vacancy = provide(RelVacancySkillDAO)
    work_schedule = provide(WorkScheduleDAO)
    employment_type = provide(EmploymentTypeDAO)
    skill = provide(SkillDAO)  # TODO split this

    create_vacancy = provide(CreateVacancyHandler)
    update_vacancy = provide(UpdateVacancyHandler)
    delete_vacancy = provide(DeleteVacancyHandler)

    get_vacancies = provide(GetVacanciesHandler)
