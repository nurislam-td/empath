from dishka import Provider, Scope, provide  # type: ignore  # noqa: PGH003

from job.common.infrastructure.repositories.vacancy import AlchemyVacancyReader, AlchemyVacancyRepo
from job.recruitment.application.commands.create_vacancy import CreateVacancyHandler
from job.recruitment.application.commands.delete_vacancy import DeleteVacancyHandler
from job.recruitment.application.commands.edit_vacancy import UpdateVacancyHandler


class RecruitmentProvider(Provider):
    scope = Scope.REQUEST

    vacancy_repo = provide(AlchemyVacancyRepo)
    vacancy_reader = provide(AlchemyVacancyReader)

    create_vacancy = provide(CreateVacancyHandler)
    update_vacancy = provide(UpdateVacancyHandler)
    delete_vacancy = provide(DeleteVacancyHandler)
