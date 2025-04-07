from collections import defaultdict
from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import RowMapping

from job.common.application.dto import SalaryDTO
from job.employment.application.dto import AuthorDTO, VacancyDTO


def convert_db_to_vacancy(  # noqa: PLR0913
    vacancy: RowMapping,
    skills: Sequence[RowMapping],
    additional_skills: Sequence[RowMapping],
    work_schedules: Sequence[RowMapping],
    employment_types: Sequence[RowMapping],
    work_formats: Sequence[RowMapping],
) -> VacancyDTO:
    return VacancyDTO(
        title=vacancy.title,
        salary=SalaryDTO(from_=vacancy.salary_from, to=vacancy.salary_to),
        address=vacancy.address,
        author=AuthorDTO(name=vacancy.company_name if vacancy.company_name else ""),
        work_exp=vacancy.work_exp,
        work_schedules=[s.name for s in work_schedules],
        employment_types=[t.name for t in employment_types],
        work_formats=[w.name for w in work_formats],
        skills=[s.name for s in skills],
        additional_skills=[s.name for s in additional_skills],
        created_at=vacancy.created_at,
        email=vacancy.email,
        status=vacancy.status,
        id=vacancy.id,
    )


def convert_db_to_vacancy_list(  # noqa: PLR0913
    vacancies: Sequence[RowMapping],
    skills: Sequence[RowMapping],
    additional_skills: Sequence[RowMapping],
    work_schedules: Sequence[RowMapping],
    employment_types: Sequence[RowMapping],
    work_formats: Sequence[RowMapping],
) -> list[VacancyDTO]:
    skill_map: dict[UUID, list[RowMapping]] = defaultdict(list)
    for skill in skills:
        skill_map[skill.vacancy_id].append(skill)

    additional_skills_map: dict[UUID, list[RowMapping]] = defaultdict(list)
    for skill in additional_skills:
        additional_skills_map[skill.vacancy_id].append(skill)

    schedule_map: dict[UUID, list[RowMapping]] = defaultdict(list)
    for schedule in work_schedules:
        schedule_map[schedule.vacancy_id].append(schedule)

    employment_map: dict[UUID, list[RowMapping]] = defaultdict(list)
    for employment in employment_types:
        employment_map[employment.vacancy_id].append(employment)

    work_format_map: dict[UUID, list[RowMapping]] = defaultdict(list)
    for work_format in work_formats:
        work_format_map[work_format.vacancy_id].append(work_format)

    return [
        convert_db_to_vacancy(
            vacancy=vacancy,
            skills=skill_map[vacancy.id],
            additional_skills=additional_skills_map[vacancy.id],
            work_schedules=schedule_map[vacancy.id],
            employment_types=employment_map[vacancy.id],
            work_formats=work_format_map[vacancy.id],
        )
        for vacancy in vacancies
    ]
