from typing import TYPE_CHECKING, Unpack, cast
from uuid import uuid4

import pytest
from dishka import AsyncContainer
from mimesis import Field, Locale, Schema

from job.employment.application.commands.create_cv import CreateCV, CreateCVHandler, Salary, Skill, WorkExp
from tests.job.employment.protocols import CVDataFactory

if TYPE_CHECKING:
    from tests.job.employment.protocols import CVData, CVDataFactory, CVDataKwargs

_ = Field(Locale.RU)


def random_salary() -> Salary:
    min_ = _("numeric.integer_number", start=150000, end=400000)
    max_ = _("numeric.integer_number", start=min_ + 10000, end=min_ + 200000)
    return Salary(from_=min_, to=max_)


def random_work_exp() -> WorkExp:
    start = _("datetime.date", start=2005, end=2020)
    end = _("datetime.date", start=start.year + 1, end=2024)
    return WorkExp(
        company_name=_("business.company"),
        title=_("person.occupation"),
        description=_("text.text", sentences=2),
        start_date=start,
        is_relevant=_("boolean"),
        end_date=end,
    )


def random_skill() -> Skill:
    return Skill(name=_("programming.language"))


@pytest.fixture
def cv_data_factory() -> "CVDataFactory":
    def factory(**kwargs: Unpack["CVDataKwargs"]) -> "CVData":
        schema = Schema(
            lambda: {
                "title": _("text.word"),
                "is_visible": _("boolean"),
                "salary": random_salary(),
                "employment_type_ids": [str(uuid4()) for _ in range(2)],
                "work_schedule_ids": [str(uuid4()) for _ in range(2)],
                "work_exp": [random_work_exp() for _ in range(2)],
                "work_formats_id": [str(uuid4()) for _ in range(2)],
                "skills": [random_skill() for _ in range(3)],
                "education": _("choice", items=["school", "bachelor", "master", "doctorate"]),
                "email": _("person.email"),
                "author_id": str(uuid4()),
                "additional_skills": [random_skill() for _ in range(2)],
                "address": _("address.address"),
                "about_me": _("text.text", sentences=3),
                "cv_file": _("internet.url"),
                "id": str(uuid4()),
            },
            iterations=1,
        )
        return cast("CVData", {**schema.create()[0]} | {**kwargs})

    return factory


@pytest.fixture
async def cv_data(cv_data_factory: CVDataFactory) -> CVData:
    return cv_data_factory()


@pytest.fixture
async def create_cv_handler(request_container: AsyncContainer) -> CreateCVHandler:
    return await request_container.get(CreateCVHandler)


async def test_create_cv_handler(create_cv_handler: CreateCVHandler, cv_data: CVData):
    await create_cv_handler(CreateCV(**cv_data))

    pass
