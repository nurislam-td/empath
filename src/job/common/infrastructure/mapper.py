from collections import defaultdict
from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import RowMapping

from job.recruitment.api.schemas import Skill
from job.recruitment.application.dto import (
    AuthorDTO,
    DetailedAuthorDTO,
    DetailedVacancyDTO,
    SalaryDTO,
    SkillDTO,
    VacancyDTO,
)


def convert_db_to_skill(skill: RowMapping) -> Skill:
    return Skill(name=skill.name, id=skill.id)


def convert_db_to_skill_dto(skill: RowMapping) -> SkillDTO:
    return SkillDTO(name=skill.name, id=skill.id)


def convert_db_detailed_vacancy(
    vacancy: RowMapping,
    skills: Sequence[RowMapping],
    additional_skills: Sequence[RowMapping],
    work_schedules: Sequence[RowMapping],
    employment_types: Sequence[RowMapping],
) -> DetailedVacancyDTO:
    return DetailedVacancyDTO(
        title=vacancy.title,
        salary=SalaryDTO(from_=vacancy.salary_from, to=vacancy.salary_to),
        address=vacancy.address,
        author=DetailedAuthorDTO(
            name=vacancy.company_name if vacancy.company_name else "",
            about_us=vacancy.about_company if vacancy.about_company else "",
        ),
        work_exp=vacancy.work_exp,
        work_schedules=[s.name for s in work_schedules],
        employment_types=[t.name for t in employment_types],
        skills=[s.name for s in skills],
        additional_skills=[s.name for s in additional_skills],
        created_at=vacancy.created_at,
        email=vacancy.email,
        id=vacancy.id,
        is_visible=vacancy.is_visible,
        work_format=vacancy.work_format,
        responsibility=vacancy.responsibility,
        requirements=vacancy.requirements,
        education=vacancy.education,
        additional_description=vacancy.additional_description,
    )


def convert_db_to_vacancy(
    vacancy: RowMapping,
    skills: Sequence[RowMapping],
    additional_skills: Sequence[RowMapping],
    work_schedules: Sequence[RowMapping],
    employment_types: Sequence[RowMapping],
) -> VacancyDTO:
    return VacancyDTO(
        title=vacancy.title,
        salary=SalaryDTO(from_=vacancy.salary_from, to=vacancy.salary_to),
        address=vacancy.address,
        author=AuthorDTO(name=vacancy.company_name if vacancy.company_name else ""),
        work_exp=vacancy.work_exp,
        work_schedules=[s.name for s in work_schedules],
        employment_types=[t.name for t in employment_types],
        skills=[s.name for s in skills],
        additional_skills=[s.name for s in additional_skills],
        created_at=vacancy.created_at,
        email=vacancy.email,
        id=vacancy.id,
    )


def convert_db_to_vacancy_list(
    vacancies: Sequence[RowMapping],
    skills: Sequence[RowMapping],
    additional_skills: Sequence[RowMapping],
    work_schedules: Sequence[RowMapping],
    employment_types: Sequence[RowMapping],
) -> list[VacancyDTO]:
    skill_map: dict[UUID, list[RowMapping]] = defaultdict(list)
    for skill in skills:
        skill_map[skill.vacancy_id].append(skill)

    additional_skills_map: dict[UUID, list[RowMapping]] = defaultdict(list)
    for skill in additional_skills:
        additional_skills_map[skill.vacancy_id].append(skill)

    schedule_map: dict[UUID, list[RowMapping]] = defaultdict(list)
    for employment in work_schedules:
        schedule_map[employment.vacancy_id].append(employment)

    employment_map: dict[UUID, list[RowMapping]] = defaultdict(list)
    for employment in employment_types:
        employment_map[employment.vacancy_id].append(employment)

    return [
        convert_db_to_vacancy(
            vacancy=vacancy,
            skills=skill_map[vacancy.id],
            additional_skills=additional_skills_map[vacancy.id],
            work_schedules=schedule_map[vacancy.id],
            employment_types=employment_map[vacancy.id],
        )
        for vacancy in vacancies
    ]
