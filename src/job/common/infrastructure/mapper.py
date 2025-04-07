from collections import defaultdict
from collections.abc import Sequence
from typing import TYPE_CHECKING

from sqlalchemy import RowMapping

from job.common.application.dto import EmploymentTypeDTO, SalaryDTO, SkillDTO, WorkFormatDTO, WorkScheduleDTO
from job.employment.application.dto import AuthorDTO as CVAuthorDTO
from job.employment.application.dto import DetailedCVDTO, VacancyResponseDTO, WorkExpDTO
from job.recruitment.application.dto import (
    AuthorDTO,
    DetailedAuthorDTO,
    DetailedVacancyDTO,
    VacancyDTO,
)

if TYPE_CHECKING:
    from uuid import UUID


def convert_db_to_skill_dto(skill: RowMapping) -> SkillDTO:
    return SkillDTO(name=skill.name, id=skill.id)


def convert_db_detailed_vacancy(  # noqa: PLR0913
    vacancy: RowMapping,
    skills: Sequence[RowMapping],
    additional_skills: Sequence[RowMapping],
    work_schedules: Sequence[RowMapping],
    employment_types: Sequence[RowMapping],
    work_formats: Sequence[RowMapping],
) -> DetailedVacancyDTO:
    return DetailedVacancyDTO(
        title=vacancy.title,
        salary=SalaryDTO(from_=vacancy.salary_from, to=vacancy.salary_to),
        address=vacancy.address,
        author=DetailedAuthorDTO(
            name=vacancy.company_name if vacancy.company_name else "",
            about_us=vacancy.about_company if vacancy.about_company else "",
            email=vacancy.company_email if vacancy.company_email else "",
        ),
        work_exp=vacancy.work_exp,
        work_schedules=[WorkScheduleDTO(name=s.name, id=s.id) for s in work_schedules],
        employment_types=[EmploymentTypeDTO(name=t.name, id=t.id) for t in employment_types],
        work_formats=[WorkFormatDTO(name=w.name, id=w.id) for w in work_formats],
        skills=[SkillDTO(name=s.name, id=s.id) for s in skills],
        additional_skills=[SkillDTO(name=s.name, id=s.id) for s in additional_skills],
        created_at=vacancy.created_at,
        email=vacancy.email,
        id=vacancy.id,
        is_visible=vacancy.is_visible,
        responsibility=vacancy.responsibility,
        requirements=vacancy.requirements,
        education=vacancy.education,
        additional_description=vacancy.additional_description,
    )


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


def convert_db_to_detailed_cv(  # noqa: PLR0913
    cv: RowMapping,
    skills: Sequence[RowMapping],
    additional_skills: Sequence[RowMapping],
    work_schedules: Sequence[RowMapping],
    employment_types: Sequence[RowMapping],
    work_formats: Sequence[RowMapping],
    work_exp: Sequence[RowMapping],
) -> DetailedCVDTO:
    return DetailedCVDTO(
        title=cv.title,
        is_visible=cv.is_visible,
        salary=SalaryDTO(from_=cv.salary_from, to=cv.salary_to),
        employment_types=[EmploymentTypeDTO(name=t.name, id=t.id) for t in employment_types],
        work_schedules=[WorkScheduleDTO(name=s.name, id=s.id) for s in work_schedules],
        work_exp=[
            WorkExpDTO(
                company_name=w.company_name,
                title=w.title,
                description=w.description,
                start_date=w.start_date,
                end_date=w.end_date,
                is_relevant=w.is_relevant,
            )
            for w in work_exp
        ],
        work_formats=[WorkFormatDTO(name=w.name, id=w.id) for w in work_formats],
        skills=[SkillDTO(name=s.name, id=s.id) for s in skills],
        education=cv.education,
        email=cv.email,
        author=CVAuthorDTO(
            name=" ".join(
                [
                    cv.author_lastname if cv.author_lastname else "",
                    cv.author_name if cv.author_name else "",
                    cv.author_patronymic if cv.author_patronymic else "",
                ],
            ),
        ),
        additional_skills=[SkillDTO(name=s.name, id=s.id) for s in additional_skills],
        address=cv.address,
        about_me=cv.about_me,
        cv_file=cv.cv_file,
        id=cv.id,
    )


def convert_db_to_vacancy_responses(response: RowMapping) -> VacancyResponseDTO:
    return VacancyResponseDTO(
        created_at=response.created_at,
        response_author=" ".join(
            [
                response.author_lastname if response.author_lastname else "",
                response.author_name if response.author_name else "",
                response.author_patronymic if response.author_patronymic else "",
            ],
        ),
        response_email=response.response_email,
        cv_title=response.cv_title,
        cv_id=response.cv_id,
        vacancy_id=response.vacancy_id,
        status=response.status,
    )
