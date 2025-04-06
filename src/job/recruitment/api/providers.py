from dishka import Provider, Scope, provide  # type: ignore  # noqa: PGH003

from job.recruitment.application.commands.create_recruiter import CreateRecruiterHandler
from job.recruitment.application.commands.create_vacancy import CreateVacancyHandler
from job.recruitment.application.commands.delete_vacancy import DeleteVacancyHandler
from job.recruitment.application.commands.edit_vacancy import UpdateVacancyHandler
from job.recruitment.infrastructure.dao.employment_type import EmploymentTypeDAO
from job.recruitment.infrastructure.dao.rel_additional_skill_vacancy import RelVacancyAdditionalSkillDAO
from job.recruitment.infrastructure.dao.rel_skill_vacancy import RelVacancySkillDAO
from job.recruitment.infrastructure.dao.skill import SkillDAO
from job.recruitment.infrastructure.dao.work_format import WorkFormatDAO
from job.recruitment.infrastructure.dao.work_schedule import WorkScheduleDAO
from job.recruitment.infrastructure.repositories.vacancy import AlchemyVacancyRepo


class RecruitmentProvider(Provider):
    scope = Scope.REQUEST

    vacancy_repo = provide(AlchemyVacancyRepo)

    rel_additional_skill_vacancy = provide(RelVacancyAdditionalSkillDAO)
    rel_skill_vacancy = provide(RelVacancySkillDAO)
    work_schedule = provide(WorkScheduleDAO)
    employment_type = provide(EmploymentTypeDAO)
    work_format = provide(WorkFormatDAO)
    skill = provide(SkillDAO)

    create_vacancy = provide(CreateVacancyHandler)
    update_vacancy = provide(UpdateVacancyHandler)
    delete_vacancy = provide(DeleteVacancyHandler)
    create_recruiter = provide(CreateRecruiterHandler)
