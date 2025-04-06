from dishka import Provider, Scope, provide

from job.common.infrastructure.repositories.cv import AlchemyCVReader, AlchemyCVRepo
from job.common.infrastructure.repositories.rel_additional_skill_cv import RelCVAdditionalSkillDAO
from job.common.infrastructure.repositories.rel_skill_cv import RelCVSkillDAO
from job.common.infrastructure.repositories.work_exp import WorkExpDAO
from job.employment.application.commands.create_cv import CreateCVHandler
from job.employment.application.queries.get_cv_by_id import GetCVByIdHandler  # type: ignore  # noqa: PGH003


class EmploymentProvider(Provider):
    scope = Scope.REQUEST

    cv_repo = provide(AlchemyCVRepo)
    cv_reader = provide(AlchemyCVReader)

    work_exp = provide(WorkExpDAO)

    rel_additional_skill_vacancy = provide(RelCVAdditionalSkillDAO)  # TODO split this
    rel_skill_vacancy = provide(RelCVSkillDAO)

    create_vacancy = provide(CreateCVHandler)

    get_cv_by_id = provide(GetCVByIdHandler)
